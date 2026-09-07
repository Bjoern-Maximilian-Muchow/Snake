#include "game_engine.h"
#include "led_grid.h"
#include "example_bot_basic.h"
#include "example_bot_safe.h"
#include "example_bot_bfs.h"
#include "perf_monitor.h"

#ifdef AUTOSNAKE_STUDENT_BOT
#include "student_bot.h"
#endif

#ifdef AUTOSNAKE_EXTERNAL_BOT
#include <string>

Direction requestExternalMove(const BotSnapshot& snapshot) {
  std::cout << "AUTOSNAKE_REQUEST {\"head\":[" << static_cast<unsigned int>(snapshot.head.x)
            << "," << static_cast<unsigned int>(snapshot.head.y)
            << "],\"food\":[" << static_cast<unsigned int>(snapshot.food.x)
            << "," << static_cast<unsigned int>(snapshot.food.y)
            << "],\"direction\":" << static_cast<unsigned int>(snapshot.currentDirection)
            << ",\"length\":" << snapshot.snakeLength
            << ",\"level\":" << static_cast<unsigned int>(snapshot.level)
            << ",\"score\":" << snapshot.score
            << ",\"body\":[";
  for (uint16_t i = 0; i < snapshot.snakeLength; ++i) {
    if (i > 0) std::cout << ',';
    const uint8_t storageIndex = static_cast<uint8_t>(snapshot.bodyStart + i);
    std::cout << static_cast<unsigned int>(snapshot.body[storageIndex]);
  }
  std::cout << "],\"occupied\":[";
  for (uint8_t i = 0; i < GRID_BITSET_BYTES; ++i) {
    if (i > 0) std::cout << ',';
    std::cout << static_cast<unsigned int>(snapshot.occupied[i]);
  }
  std::cout << "],\"obstacles\":[";
  for (uint8_t i = 0; i < GRID_BITSET_BYTES; ++i) {
    if (i > 0) std::cout << ',';
    std::cout << static_cast<unsigned int>(snapshot.obstacles[i]);
  }
  std::cout << "]}\n" << std::flush;

  std::string response;
  if (!std::getline(std::cin, response)) return snapshot.currentDirection;
  const std::string prefix = "AUTOSNAKE_MOVE ";
  if (response.rfind(prefix, 0) != 0) return snapshot.currentDirection;
  const char move = response[prefix.size()];
  if (move == '0') return DIR_UP;
  if (move == '1') return DIR_RIGHT;
  if (move == '2') return DIR_DOWN;
  if (move == '3') return DIR_LEFT;
  return snapshot.currentDirection;
}
#endif

GameEngine engine;
LedGrid ledGrid;
PerfMonitor perf;
unsigned long lastStep = 0;
StepResult lastResult = STEP_OK;

Direction chooseMove(const BotSnapshot& snapshot) {
#ifdef AUTOSNAKE_EXTERNAL_BOT
  return requestExternalMove(snapshot);
#elif defined(AUTOSNAKE_STUDENT_BOT)
  return chooseStudentMove(snapshot);
#else
  if (snapshot.level == 1) {
    return chooseBasicMove(snapshot);
  }
  if (snapshot.level == 2) {
    return chooseSafeMove(snapshot);
  }
  return chooseBfsMove(snapshot);
#endif
}

void printHelp() {
  Serial.println(F("Befehle: 1/2/3=Level, r=Reset, c=CSV/Text, h=Hilfe"));
}

void resetLevel(uint8_t level) {
  engine.reset(level);
  perf.resetCounters();
  lastResult = STEP_OK;
  ledGrid.render(engine);
  Serial.print(F("Level "));
  Serial.print(level);
  Serial.println(F(" gestartet"));
}

void handleSerial() {
  while (Serial.available() > 0) {
    char command = Serial.read();
    if (command >= '1' && command <= '3') {
      resetLevel(command - '0');
    } else if (command == 'r' || command == 'R') {
      resetLevel(engine.level());
    } else if (command == 'c' || command == 'C') {
      perf.toggleCsv(Serial);
    } else if (command == 'h' || command == 'H') {
      printHelp();
    }
  }
}

void setup() {
  Serial.begin(SERIAL_BAUD);
  Serial.println(F("AutoSnake Uno startet"));
  Serial.println(F("Keine externen Bibliotheken, Live-Telemetrie aktiv"));
  printHelp();
  engine.reset(DEFAULT_LEVEL);
  ledGrid.begin();
  perf.begin();
  ledGrid.render(engine);
}

void loop() {
  handleSerial();

  unsigned long now = millis();
  if (now - lastStep < STEP_DELAY_MS) {
    return;
  }
  lastStep = now;

  uint32_t startedAt = micros();
  Direction move = chooseMove(engine.snapshot());
  uint32_t afterBot = micros();
  lastResult = engine.step(move);
  uint32_t afterEngine = micros();
  ledGrid.render(engine);
  uint32_t afterRender = micros();

  perf.recordStep(afterBot - startedAt, afterEngine - afterBot, afterRender - afterEngine, lastResult);
#ifdef AUTOSNAKE_VIRTUAL
  virtualMonitorEmit(
    engine.level(), engine.score(), engine.length(),
    afterBot - startedAt, afterEngine - afterBot, afterRender - afterEngine,
    static_cast<int>(lastResult)
  );
#endif

  if (perf.due(now)) {
    perf.print(Serial, engine, lastResult);
    perf.markPrinted(now);
  }

  if (lastResult >= STEP_WALL_COLLISION) {
    perf.print(Serial, engine, lastResult);
    Serial.println(F("Spielende, Reset in 1s"));
    delay(1000);
    resetLevel(engine.level());
  }
}

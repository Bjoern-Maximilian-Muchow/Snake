#include "game_engine.h"
#include "led_grid.h"
#include "example_bot_basic.h"
#include "example_bot_safe.h"
#include "example_bot_bfs.h"
#include "perf_monitor.h"

GameEngine engine;
LedGrid ledGrid;
PerfMonitor perf;
unsigned long lastStep = 0;
StepResult lastResult = STEP_OK;

Direction chooseMove(const BotSnapshot& snapshot) {
  if (snapshot.level == 1) {
    return chooseBasicMove(snapshot);
  }
  if (snapshot.level == 2) {
    return chooseSafeMove(snapshot);
  }
  return chooseBfsMove(snapshot);
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

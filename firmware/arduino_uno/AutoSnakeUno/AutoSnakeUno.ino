#include "game_engine.h"
#include "led_grid.h"
#include "example_bot_basic.h"
#include "perf_monitor.h"

GameEngine engine;
LedGrid ledGrid;
PerfMonitor perf;
unsigned long lastStep = 0;
StepResult lastResult = STEP_OK;

void setup() {
  Serial.begin(SERIAL_BAUD);
  while (!Serial) {
    ; 
  }
  Serial.println(F("AutoSnake Uno startet"));
  Serial.println(F("Keine externen Bibliotheken, serielle Live-Statistik aktiv"));
  engine.reset();
  ledGrid.begin();
  perf.begin();
  ledGrid.render(engine);
}

void loop() {
  unsigned long now = millis();
  if (now - lastStep < STEP_DELAY_MS) {
    return;
  }
  lastStep = now;

  uint32_t startedAt = micros();
  Direction move = chooseBasicMove(engine.snapshot());
  lastResult = engine.step(move);
  ledGrid.render(engine);
  uint32_t stepDuration = micros() - startedAt;
  perf.recordStep(stepDuration);

  if (perf.due(now)) {
    perf.print(Serial, engine, lastResult);
    perf.markPrinted(now);
  }

  if (lastResult == STEP_WALL_COLLISION || lastResult == STEP_SELF_COLLISION) {
    Serial.println(F("Spielende, Reset in 1s"));
    delay(1000);
    engine.reset();
    lastResult = STEP_OK;
  }
}

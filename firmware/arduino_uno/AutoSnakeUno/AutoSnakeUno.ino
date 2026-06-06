#include "game_engine.h"
#include "led_grid.h"
#include "example_bot_basic.h"

GameEngine engine;
LedGrid ledGrid;
unsigned long lastStep = 0;

void setup() {
  Serial.begin(9600);
  engine.reset();
  ledGrid.begin();
  ledGrid.render(engine);
}

void loop() {
  unsigned long now = millis();
  if (now - lastStep < STEP_DELAY_MS) {
    return;
  }
  lastStep = now;

  Direction move = chooseBasicMove(engine.snapshot());
  StepResult result = engine.step(move);
  ledGrid.render(engine);

  if (result == STEP_COLLISION) {
    Serial.println("Game over");
    delay(1000);
    engine.reset();
  }
}

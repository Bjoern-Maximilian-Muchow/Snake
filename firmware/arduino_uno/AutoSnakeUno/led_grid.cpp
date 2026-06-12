#include "led_grid.h"

void LedGrid::begin() {
  pinMode(LED_BUILTIN, OUTPUT);
  clear();
}

void LedGrid::clear() {
  digitalWrite(LED_BUILTIN, LOW);
}

void LedGrid::render(const GameEngine& engine) {
  digitalWrite(LED_BUILTIN, engine.gameOver() ? HIGH : LOW);
  const Point* snake = engine.body();
  for (uint8_t i = 0; i < engine.length(); ++i) {
    setPixel(snake[i].x, snake[i].y, i == 0 ? 0 : 0, i == 0 ? 255 : 80, 0);
  }
  BotSnapshot snapshot = engine.snapshot();
  setPixel(snapshot.food.x, snapshot.food.y, 255, 0, 0);
}

void LedGrid::setPixel(uint8_t x, uint8_t y, uint8_t r, uint8_t g, uint8_t b) {
  (void)x;
  (void)y;
  (void)r;
  (void)g;
  (void)b;
  // Platzhalter für die hardwarespezifische Pixelausgabe.
}

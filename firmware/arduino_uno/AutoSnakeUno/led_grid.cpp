#include "led_grid.h"

void LedGrid::begin() {
  clear();
}

void LedGrid::clear() {
  // Placeholder for future RGB LED grid driver initialization.
}

void LedGrid::render(const GameEngine& engine) {
  clear();
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
  // Placeholder for hardware-specific pixel output.
}

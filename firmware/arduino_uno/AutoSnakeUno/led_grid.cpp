#include "led_grid.h"

void LedGrid::begin() {
  pinMode(LED_BUILTIN, OUTPUT);
#ifdef AUTOSNAKE_VIRTUAL
  virtualLedGridBegin();
#endif
  clear();
}

void LedGrid::clear() {
  digitalWrite(LED_BUILTIN, LOW);
#ifdef AUTOSNAKE_VIRTUAL
  virtualLedGridClear();
#endif
}

void LedGrid::render(const GameEngine& engine) {
  digitalWrite(LED_BUILTIN, engine.gameOver() ? HIGH : LOW);
  for (uint16_t i = 0; i < engine.length(); ++i) {
    Point segment = engine.bodyPoint(i);
    setPixel(segment.x, segment.y, 0, i == 0 ? 255 : 80, 0);
  }
  BotSnapshot snapshot = engine.snapshot();
  setPixel(snapshot.food.x, snapshot.food.y, 255, 0, 0);
#ifdef AUTOSNAKE_VIRTUAL
  virtualLedGridPresent();
#endif
}

void LedGrid::setPixel(uint8_t x, uint8_t y, uint8_t r, uint8_t g, uint8_t b) {
#ifdef AUTOSNAKE_VIRTUAL
  virtualLedGridSetPixel(x, y, r, g, b);
#else
  (void)x;
  (void)y;
  (void)r;
  (void)g;
  (void)b;
  // Platzhalter für die hardwarespezifische Pixelausgabe.
#endif
}

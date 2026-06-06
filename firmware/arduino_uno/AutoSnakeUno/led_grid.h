#ifndef AUTOSNAKE_LED_GRID_H
#define AUTOSNAKE_LED_GRID_H

#include "game_engine.h"

class LedGrid {
public:
  void begin();
  void clear();
  void render(const GameEngine& engine);

private:
  void setPixel(uint8_t x, uint8_t y, uint8_t r, uint8_t g, uint8_t b);
};

#endif

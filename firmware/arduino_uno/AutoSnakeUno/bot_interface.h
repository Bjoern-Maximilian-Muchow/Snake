#ifndef AUTOSNAKE_BOT_INTERFACE_H
#define AUTOSNAKE_BOT_INTERFACE_H

#include "config.h"

enum Direction : uint8_t {
  DIR_UP = 0,
  DIR_RIGHT = 1,
  DIR_DOWN = 2,
  DIR_LEFT = 3
};

struct Point {
  uint8_t x;
  uint8_t y;
};

struct BotSnapshot {
  Point head;
  Point food;
  Direction currentDirection;
  uint8_t snakeLength;
};

typedef Direction (*BotDecisionFn)(const BotSnapshot& snapshot);

inline bool isOpposite(Direction a, Direction b) {
  return (a == DIR_UP && b == DIR_DOWN) ||
         (a == DIR_DOWN && b == DIR_UP) ||
         (a == DIR_LEFT && b == DIR_RIGHT) ||
         (a == DIR_RIGHT && b == DIR_LEFT);
}

#endif

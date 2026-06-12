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
  uint16_t snakeLength;
  uint8_t level;
  const uint8_t* occupied;
  const uint8_t* obstacles;
};

typedef Direction (*BotDecisionFn)(const BotSnapshot& snapshot);

inline bool isOpposite(Direction a, Direction b) {
  return (a == DIR_UP && b == DIR_DOWN) ||
         (a == DIR_DOWN && b == DIR_UP) ||
         (a == DIR_LEFT && b == DIR_RIGHT) ||
         (a == DIR_RIGHT && b == DIR_LEFT);
}

inline uint8_t packPoint(Point point) {
  return (point.y << 4) | point.x;
}

inline Point unpackPoint(uint8_t packed) {
  Point point = {static_cast<uint8_t>(packed & 0x0F), static_cast<uint8_t>(packed >> 4)};
  return point;
}

inline bool pointEquals(Point a, Point b) {
  return a.x == b.x && a.y == b.y;
}

inline bool pointInside(Point point) {
  return point.x < GRID_WIDTH && point.y < GRID_HEIGHT;
}

inline Point movedPoint(Point point, Direction direction) {
  if (direction == DIR_UP) {
    point.y--;
  } else if (direction == DIR_RIGHT) {
    point.x++;
  } else if (direction == DIR_DOWN) {
    point.y++;
  } else {
    point.x--;
  }
  return point;
}

inline bool bitsetContains(const uint8_t* bitset, Point point) {
  if (!pointInside(point)) {
    return false;
  }
  uint8_t packed = packPoint(point);
  return (bitset[packed >> 3] & _BV(packed & 0x07)) != 0;
}

inline bool snapshotBlocked(const BotSnapshot& snapshot, Point point) {
  return !pointInside(point) ||
         bitsetContains(snapshot.occupied, point) ||
         bitsetContains(snapshot.obstacles, point);
}

#endif

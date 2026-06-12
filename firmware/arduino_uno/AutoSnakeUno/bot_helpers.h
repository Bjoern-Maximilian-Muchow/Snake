#ifndef AUTOSNAKE_BOT_HELPERS_H
#define AUTOSNAKE_BOT_HELPERS_H

#include "bot_interface.h"

inline bool isSafeMove(const BotSnapshot& snapshot, Direction move) {
  if (isOpposite(move, snapshot.currentDirection)) {
    return false;
  }
  Point next = movedPoint(snapshot.head, move);
  return !snapshotBlocked(snapshot, next);
}

inline uint8_t foodFirstMoves(const BotSnapshot& snapshot, Direction* moves) {
  uint8_t count = 0;

  if (snapshot.food.x > snapshot.head.x) {
    moves[count++] = DIR_RIGHT;
  } else if (snapshot.food.x < snapshot.head.x) {
    moves[count++] = DIR_LEFT;
  }
  if (snapshot.food.y > snapshot.head.y) {
    moves[count++] = DIR_DOWN;
  } else if (snapshot.food.y < snapshot.head.y) {
    moves[count++] = DIR_UP;
  }

  const Direction fallback[] = {DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT};
  for (uint8_t i = 0; i < 4; ++i) {
    bool alreadyAdded = false;
    for (uint8_t j = 0; j < count; ++j) {
      if (moves[j] == fallback[i]) {
        alreadyAdded = true;
        break;
      }
    }
    if (!alreadyAdded) {
      moves[count++] = fallback[i];
    }
  }
  return count;
}

inline void visitedSet(uint8_t* visited, Point point) {
  uint8_t packed = packPoint(point);
  visited[packed >> 3] |= _BV(packed & 0x07);
}

inline bool visitedContains(const uint8_t* visited, Point point) {
  return bitsetContains(visited, point);
}

#endif

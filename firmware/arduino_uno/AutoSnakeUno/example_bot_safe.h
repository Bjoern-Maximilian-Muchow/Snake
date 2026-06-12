#ifndef AUTOSNAKE_EXAMPLE_BOT_SAFE_H
#define AUTOSNAKE_EXAMPLE_BOT_SAFE_H

#include "bot_helpers.h"

inline Direction chooseSafeMove(const BotSnapshot& snapshot) {
  Direction moves[4];
  uint8_t moveCount = foodFirstMoves(snapshot, moves);
  for (uint8_t i = 0; i < moveCount; ++i) {
    if (isSafeMove(snapshot, moves[i])) {
      return moves[i];
    }
  }
  return snapshot.currentDirection;
}

#endif

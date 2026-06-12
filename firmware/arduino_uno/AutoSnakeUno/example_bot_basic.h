#ifndef AUTOSNAKE_EXAMPLE_BOT_BASIC_H
#define AUTOSNAKE_EXAMPLE_BOT_BASIC_H

#include "bot_interface.h"

inline Direction chooseBasicMove(const BotSnapshot& snapshot) {
  Direction preferred = snapshot.currentDirection;

  if (snapshot.food.x > snapshot.head.x) {
    preferred = DIR_RIGHT;
  } else if (snapshot.food.x < snapshot.head.x) {
    preferred = DIR_LEFT;
  } else if (snapshot.food.y > snapshot.head.y) {
    preferred = DIR_DOWN;
  } else if (snapshot.food.y < snapshot.head.y) {
    preferred = DIR_UP;
  }

  return isOpposite(preferred, snapshot.currentDirection)
    ? snapshot.currentDirection
    : preferred;
}

#endif

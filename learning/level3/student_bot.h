#ifndef AUTOSNAKE_STUDENT_BOT_H
#define AUTOSNAKE_STUDENT_BOT_H

#include "bot_interface.h"

inline Direction chooseStudentMove(const BotSnapshot& snapshot) {
  // TODO: Sichere, zeitlich begrenzte Strategie implementieren.
  // Keine dynamische Speicherallokation verwenden.
  return snapshot.currentDirection;
}

#endif

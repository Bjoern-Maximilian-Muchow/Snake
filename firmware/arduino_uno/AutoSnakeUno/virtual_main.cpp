#ifdef AUTOSNAKE_VIRTUAL

#include "config.h"
#include "AutoSnakeUno.ino"

int main() {
  setup();
#ifdef AUTOSNAKE_VIRTUAL_LEVEL
  resetLevel(AUTOSNAKE_VIRTUAL_LEVEL);
#endif
  for (uint16_t step = 0; step < 100; ++step) {
    loop();
    delay(STEP_DELAY_MS);
  }
  return virtualBudgetFailed() ? 3 : 0;
}

#endif
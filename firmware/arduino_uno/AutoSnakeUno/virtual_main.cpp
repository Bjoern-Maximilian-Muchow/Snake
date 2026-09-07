#ifdef AUTOSNAKE_VIRTUAL

#include "config.h"
#include "AutoSnakeUno.ino"

int main() {
  setup();
  for (uint16_t step = 0; step < 100; ++step) {
    loop();
    delay(STEP_DELAY_MS);
  }
  return 0;
}

#endif
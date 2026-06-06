# Arduino Uno Firmware

This folder contains the first Arduino Uno R3 firmware skeleton for AutoSnake Remote Lab.

The code is intentionally small and split into:

- `game_engine.*`: hardware-independent Snake state and update logic.
- `bot_interface.h`: compact snapshot and move API.
- `example_bot_basic.h`: simple rule-based example bot.
- `led_grid.*`: LED output abstraction placeholder.
- `AutoSnakeUno.ino`: Arduino entry point.

The Arduino Uno has limited RAM, so the firmware avoids dynamic allocation and stores the snake body in fixed-size arrays.

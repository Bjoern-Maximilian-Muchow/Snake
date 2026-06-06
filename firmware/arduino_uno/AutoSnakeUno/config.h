#ifndef AUTOSNAKE_CONFIG_H
#define AUTOSNAKE_CONFIG_H

#include <Arduino.h>

const uint8_t GRID_WIDTH = 16;
const uint8_t GRID_HEIGHT = 16;
const uint16_t GRID_CELLS = GRID_WIDTH * GRID_HEIGHT;
const unsigned long STEP_DELAY_MS = 180;

#endif

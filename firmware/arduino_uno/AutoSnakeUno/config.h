#ifndef AUTOSNAKE_CONFIG_H
#define AUTOSNAKE_CONFIG_H

#include <Arduino.h>

const uint8_t GRID_WIDTH = 16;
const uint8_t GRID_HEIGHT = 16;
const uint16_t GRID_CELLS = GRID_WIDTH * GRID_HEIGHT;
const unsigned long STEP_DELAY_MS = 180;
const unsigned long STATS_INTERVAL_MS = 1000;
const uint32_t SERIAL_BAUD = 115200;

#endif

#ifndef AUTOSNAKE_CONFIG_H
#define AUTOSNAKE_CONFIG_H

#include <Arduino.h>

const uint8_t GRID_WIDTH = 16;
const uint8_t GRID_HEIGHT = 16;
const uint16_t GRID_CELLS = GRID_WIDTH * GRID_HEIGHT;
const uint8_t GRID_BITSET_BYTES = GRID_CELLS / 8;

const uint8_t DEFAULT_LEVEL = 1;
const uint8_t BFS_MAX_NODES = 64;
const uint16_t BOT_TIME_LIMIT_US = 3000;
const uint16_t BOT_TIME_GUARD_US = 150;

const unsigned long STEP_DELAY_MS = 180;
const unsigned long STATS_INTERVAL_MS = 1000;
const uint32_t SERIAL_BAUD = 115200;

#endif

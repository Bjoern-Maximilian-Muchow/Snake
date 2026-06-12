#ifndef AUTOSNAKE_EXAMPLE_BOT_BFS_H
#define AUTOSNAKE_EXAMPLE_BOT_BFS_H

#include "bot_helpers.h"
#include "example_bot_safe.h"

static uint8_t bfsQueuePosition[BFS_MAX_NODES];
static uint8_t bfsQueueFirstMove[BFS_MAX_NODES];
static uint8_t bfsVisited[GRID_BITSET_BYTES];

inline bool hasReachableSpace(const BotSnapshot& snapshot, Direction firstMove, uint32_t deadline) {
  Point start = movedPoint(snapshot.head, firstMove);
  if (snapshotBlocked(snapshot, start)) {
    return false;
  }

  memset(bfsVisited, 0, GRID_BITSET_BYTES);
  uint8_t readIndex = 0;
  uint8_t writeIndex = 0;
  uint8_t queued = 0;
  uint8_t reached = 0;
  uint16_t desired = snapshot.snakeLength + 4;
  uint8_t required = snapshot.snakeLength < 8 ? 8 : static_cast<uint8_t>(desired > 24 ? 24 : desired);

  bfsQueuePosition[writeIndex++] = packPoint(start);
  queued++;
  visitedSet(bfsVisited, start);

  while (queued > 0 && reached < required && static_cast<int32_t>(deadline - micros()) > 0) {
    Point current = unpackPoint(bfsQueuePosition[readIndex++]);
    if (readIndex == BFS_MAX_NODES) {
      readIndex = 0;
    }
    queued--;
    reached++;

    for (uint8_t rawMove = 0; rawMove < 4; ++rawMove) {
      Point next = movedPoint(current, static_cast<Direction>(rawMove));
      if (!pointInside(next) || snapshotBlocked(snapshot, next) || visitedContains(bfsVisited, next)) {
        continue;
      }
      if (queued >= BFS_MAX_NODES) {
        return reached >= required;
      }
      bfsQueuePosition[writeIndex++] = packPoint(next);
      if (writeIndex == BFS_MAX_NODES) {
        writeIndex = 0;
      }
      queued++;
      visitedSet(bfsVisited, next);
    }
  }

  return reached >= required;
}

inline Direction chooseBfsMove(const BotSnapshot& snapshot) {
  const uint32_t deadline = micros() + BOT_TIME_LIMIT_US - BOT_TIME_GUARD_US;
  memset(bfsVisited, 0, GRID_BITSET_BYTES);
  uint8_t readIndex = 0;
  uint8_t writeIndex = 0;
  uint8_t queued = 0;

  visitedSet(bfsVisited, snapshot.head);
  for (uint8_t rawMove = 0; rawMove < 4; ++rawMove) {
    Direction move = static_cast<Direction>(rawMove);
    if (!isSafeMove(snapshot, move)) {
      continue;
    }
    Point next = movedPoint(snapshot.head, move);
    bfsQueuePosition[writeIndex] = packPoint(next);
    bfsQueueFirstMove[writeIndex] = rawMove;
    writeIndex++;
    queued++;
    visitedSet(bfsVisited, next);
  }

  while (queued > 0 && static_cast<int32_t>(deadline - micros()) > 0) {
    Point current = unpackPoint(bfsQueuePosition[readIndex]);
    Direction firstMove = static_cast<Direction>(bfsQueueFirstMove[readIndex]);
    readIndex++;
    if (readIndex == BFS_MAX_NODES) {
      readIndex = 0;
    }
    queued--;

    if (pointEquals(current, snapshot.food) && hasReachableSpace(snapshot, firstMove, deadline)) {
      return firstMove;
    }

    for (uint8_t rawMove = 0; rawMove < 4; ++rawMove) {
      Point next = movedPoint(current, static_cast<Direction>(rawMove));
      if (!pointInside(next) || snapshotBlocked(snapshot, next) || visitedContains(bfsVisited, next)) {
        continue;
      }
      if (queued >= BFS_MAX_NODES) {
        return chooseSafeMove(snapshot);
      }
      bfsQueuePosition[writeIndex] = packPoint(next);
      bfsQueueFirstMove[writeIndex] = static_cast<uint8_t>(firstMove);
      writeIndex++;
      if (writeIndex == BFS_MAX_NODES) {
        writeIndex = 0;
      }
      queued++;
      visitedSet(bfsVisited, next);
    }
  }

  return chooseSafeMove(snapshot);
}

#endif

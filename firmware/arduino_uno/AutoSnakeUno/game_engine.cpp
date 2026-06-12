#include "game_engine.h"

GameEngine::GameEngine() {
  reset();
}

void GameEngine::reset(uint8_t level) {
  currentLevel = constrain(level, 1, 3);
  clearBitset(occupied);
  clearBitset(obstacles);
  configureObstacles();

  headIndex = 0;
  snakeLength = 3;
  body[0] = packPoint({8, 8});
  body[1] = packPoint({7, 8});
  body[2] = packPoint({6, 8});
  setBit(occupied, {8, 8});
  setBit(occupied, {7, 8});
  setBit(occupied, {6, 8});

  direction = DIR_RIGHT;
  food = {12, 8};
  if (isObstacle(food)) {
    placeFood();
  }
  currentScore = 0;
  over = false;
}

StepResult GameEngine::step(Direction requestedDirection) {
  if (over) {
    return STEP_SELF_COLLISION;
  }

  if (!isOpposite(requestedDirection, direction)) {
    direction = requestedDirection;
  }

  Point head = nextHead(direction);
  if (isWall(head)) {
    over = true;
    return STEP_WALL_COLLISION;
  }
  if (isObstacle(head)) {
    over = true;
    return STEP_OBSTACLE_COLLISION;
  }

  bool ateFood = pointEquals(head, food);
  Point tail = bodyPoint(snakeLength - 1);
  bool movingIntoReleasedTail = !ateFood && pointEquals(head, tail);
  if (isOccupied(head) && !movingIntoReleasedTail) {
    over = true;
    return STEP_SELF_COLLISION;
  }

  if (!ateFood) {
    clearBit(occupied, tail);
  }

  headIndex--;
  body[headIndex] = packPoint(head);
  setBit(occupied, head);

  if (ateFood) {
    if (snakeLength < GRID_CELLS) {
      snakeLength++;
    }
    currentScore++;
    placeFood();
    return STEP_ATE_FOOD;
  }

  return STEP_OK;
}

BotSnapshot GameEngine::snapshot() const {
  BotSnapshot result;
  result.head = bodyPoint(0);
  result.food = food;
  result.currentDirection = direction;
  result.snakeLength = snakeLength;
  result.level = currentLevel;
  result.occupied = occupied;
  result.obstacles = obstacles;
  return result;
}

Point GameEngine::bodyPoint(uint16_t index) const {
  uint8_t storageIndex = headIndex + static_cast<uint8_t>(index);
  return unpackPoint(body[storageIndex]);
}

uint16_t GameEngine::length() const {
  return snakeLength;
}

uint16_t GameEngine::score() const {
  return currentScore;
}

uint8_t GameEngine::level() const {
  return currentLevel;
}

bool GameEngine::gameOver() const {
  return over;
}

bool GameEngine::isOccupied(Point point) const {
  return bitsetContains(occupied, point);
}

bool GameEngine::isObstacle(Point point) const {
  return bitsetContains(obstacles, point);
}

void GameEngine::clearBitset(uint8_t* bitset) {
  memset(bitset, 0, GRID_BITSET_BYTES);
}

void GameEngine::setBit(uint8_t* bitset, Point point) {
  uint8_t packed = packPoint(point);
  bitset[packed >> 3] |= _BV(packed & 0x07);
}

void GameEngine::clearBit(uint8_t* bitset, Point point) {
  uint8_t packed = packPoint(point);
  bitset[packed >> 3] &= static_cast<uint8_t>(~_BV(packed & 0x07));
}

void GameEngine::configureObstacles() {
  if (currentLevel < 2) {
    return;
  }

  const Point levelTwo[] = {
    {5, 4}, {5, 5}, {5, 6}, {10, 9}, {11, 9}, {12, 9}
  };
  for (uint8_t i = 0; i < sizeof(levelTwo) / sizeof(levelTwo[0]); ++i) {
    setBit(obstacles, levelTwo[i]);
  }

  if (currentLevel == 3) {
    const Point levelThree[] = {
      {3, 11}, {4, 11}, {5, 11}, {9, 3}, {9, 4}
    };
    for (uint8_t i = 0; i < sizeof(levelThree) / sizeof(levelThree[0]); ++i) {
      setBit(obstacles, levelThree[i]);
    }
  }
}

bool GameEngine::isWall(Point point) const {
  return !pointInside(point);
}

Point GameEngine::nextHead(Direction nextDirection) const {
  return movedPoint(bodyPoint(0), nextDirection);
}

void GameEngine::placeFood() {
  for (uint16_t packed = 0; packed < GRID_CELLS; ++packed) {
    Point candidate = unpackPoint(static_cast<uint8_t>(packed));
    if (!isOccupied(candidate) && !isObstacle(candidate)) {
      food = candidate;
      return;
    }
  }
}

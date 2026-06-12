#ifndef AUTOSNAKE_GAME_ENGINE_H
#define AUTOSNAKE_GAME_ENGINE_H

#include "bot_interface.h"

enum StepResult : uint8_t {
  STEP_OK = 0,
  STEP_ATE_FOOD = 1,
  STEP_WALL_COLLISION = 2,
  STEP_SELF_COLLISION = 3,
  STEP_OBSTACLE_COLLISION = 4
};

class GameEngine {
public:
  GameEngine();
  void reset(uint8_t level = DEFAULT_LEVEL);
  StepResult step(Direction requestedDirection);
  BotSnapshot snapshot() const;
  Point bodyPoint(uint16_t index) const;
  uint16_t length() const;
  uint16_t score() const;
  uint8_t level() const;
  bool gameOver() const;
  bool isOccupied(Point point) const;
  bool isObstacle(Point point) const;

private:
  uint8_t body[GRID_CELLS];
  uint8_t occupied[GRID_BITSET_BYTES];
  uint8_t obstacles[GRID_BITSET_BYTES];
  uint8_t headIndex;
  uint16_t snakeLength;
  Direction direction;
  Point food;
  uint16_t currentScore;
  uint8_t currentLevel;
  bool over;

  void clearBitset(uint8_t* bitset);
  void setBit(uint8_t* bitset, Point point);
  void clearBit(uint8_t* bitset, Point point);
  void configureObstacles();
  bool isWall(Point point) const;
  Point nextHead(Direction nextDirection) const;
  void placeFood();
};

#endif

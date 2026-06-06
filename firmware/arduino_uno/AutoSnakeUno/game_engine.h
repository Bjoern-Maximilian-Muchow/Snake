#ifndef AUTOSNAKE_GAME_ENGINE_H
#define AUTOSNAKE_GAME_ENGINE_H

#include "bot_interface.h"

enum StepResult : uint8_t {
  STEP_OK = 0,
  STEP_ATE_FOOD = 1,
  STEP_COLLISION = 2
};

class GameEngine {
public:
  GameEngine();
  void reset();
  StepResult step(Direction requestedDirection);
  BotSnapshot snapshot() const;
  const Point* body() const;
  uint8_t length() const;
  uint16_t score() const;
  bool gameOver() const;

private:
  Point snake[GRID_CELLS];
  uint8_t snakeLength;
  Direction direction;
  Point food;
  uint16_t currentScore;
  bool over;

  bool contains(Point p) const;
  bool isWall(Point p) const;
  Point nextHead(Direction nextDirection) const;
  void placeFood();
};

#endif

#include "game_engine.h"

GameEngine::GameEngine() {
  reset();
}

void GameEngine::reset() {
  snakeLength = 3;
  snake[0] = {8, 8};
  snake[1] = {7, 8};
  snake[2] = {6, 8};
  direction = DIR_RIGHT;
  food = {12, 8};
  currentScore = 0;
  over = false;
}

StepResult GameEngine::step(Direction requestedDirection) {
  if (over) {
    return STEP_COLLISION;
  }

  if (!isOpposite(requestedDirection, direction)) {
    direction = requestedDirection;
  }

  Point head = nextHead(direction);
  if (isWall(head) || contains(head)) {
    over = true;
    return STEP_COLLISION;
  }

  bool ateFood = (head.x == food.x && head.y == food.y);
  uint8_t newLength = snakeLength;
  if (ateFood && snakeLength < GRID_CELLS) {
    newLength++;
  }

  for (int i = newLength - 1; i > 0; --i) {
    snake[i] = snake[i - 1];
  }
  snake[0] = head;
  snakeLength = newLength;

  if (ateFood) {
    currentScore++;
    placeFood();
    return STEP_ATE_FOOD;
  }

  return STEP_OK;
}

BotSnapshot GameEngine::snapshot() const {
  BotSnapshot s;
  s.head = snake[0];
  s.food = food;
  s.currentDirection = direction;
  s.snakeLength = snakeLength;
  return s;
}

const Point* GameEngine::body() const {
  return snake;
}

uint8_t GameEngine::length() const {
  return snakeLength;
}

uint16_t GameEngine::score() const {
  return currentScore;
}

bool GameEngine::gameOver() const {
  return over;
}

bool GameEngine::contains(Point p) const {
  for (uint8_t i = 0; i < snakeLength; ++i) {
    if (snake[i].x == p.x && snake[i].y == p.y) {
      return true;
    }
  }
  return false;
}

bool GameEngine::isWall(Point p) const {
  return p.x >= GRID_WIDTH || p.y >= GRID_HEIGHT;
}

Point GameEngine::nextHead(Direction nextDirection) const {
  Point head = snake[0];
  if (nextDirection == DIR_UP) {
    head.y--;
  } else if (nextDirection == DIR_DOWN) {
    head.y++;
  } else if (nextDirection == DIR_LEFT) {
    head.x--;
  } else if (nextDirection == DIR_RIGHT) {
    head.x++;
  }
  return head;
}

void GameEngine::placeFood() {
  for (uint8_t y = 0; y < GRID_HEIGHT; ++y) {
    for (uint8_t x = 0; x < GRID_WIDTH; ++x) {
      Point candidate = {x, y};
      if (!contains(candidate)) {
        food = candidate;
        return;
      }
    }
  }
}

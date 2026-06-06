from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


GRID_WIDTH = 16
GRID_HEIGHT = 16


class Direction(str, Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass(frozen=True)
class BotSnapshot:
    head: Point
    food: Point
    direction: Direction
    snake: tuple[Point, ...]
    obstacles: tuple[Point, ...]
    score: int


class StepResult(str, Enum):
    OK = "ok"
    ATE_FOOD = "ate_food"
    WALL_COLLISION = "wall_collision"
    SELF_COLLISION = "self_collision"
    OBSTACLE_COLLISION = "obstacle_collision"


OPPOSITES = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


DELTAS = {
    Direction.UP: (0, -1),
    Direction.RIGHT: (1, 0),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
}


class GameEngine:
    def __init__(
        self,
        width: int = GRID_WIDTH,
        height: int = GRID_HEIGHT,
        snake: list[Point] | None = None,
        food: Point | None = None,
        obstacles: set[Point] | None = None,
        direction: Direction = Direction.RIGHT,
    ) -> None:
        self.width = width
        self.height = height
        self.snake = snake or [Point(8, 8), Point(7, 8), Point(6, 8)]
        self.food = food or Point(12, 8)
        self.obstacles = obstacles or set()
        self.direction = direction
        self.score = 0
        self.game_over = False
        self.last_result = StepResult.OK

    def snapshot(self) -> BotSnapshot:
        return BotSnapshot(
            head=self.snake[0],
            food=self.food,
            direction=self.direction,
            snake=tuple(self.snake),
            obstacles=tuple(sorted(self.obstacles, key=lambda point: (point.y, point.x))),
            score=self.score,
        )

    def is_inside(self, point: Point) -> bool:
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def next_head(self, direction: Direction) -> Point:
        dx, dy = DELTAS[direction]
        head = self.snake[0]
        return Point(head.x + dx, head.y + dy)

    def valid_moves(self) -> list[Direction]:
        moves: list[Direction] = []
        for direction in Direction:
            if direction == OPPOSITES[self.direction]:
                continue
            head = self.next_head(direction)
            tail_safe_body = set(self.snake[:-1])
            if self.is_inside(head) and head not in tail_safe_body and head not in self.obstacles:
                moves.append(direction)
        return moves

    def step(self, requested_direction: Direction) -> StepResult:
        if self.game_over:
            return self.last_result

        if requested_direction != OPPOSITES[self.direction]:
            self.direction = requested_direction

        head = self.next_head(self.direction)
        if not self.is_inside(head):
            return self._finish(StepResult.WALL_COLLISION)
        if head in self.obstacles:
            return self._finish(StepResult.OBSTACLE_COLLISION)

        will_grow = head == self.food
        occupied = set(self.snake if will_grow else self.snake[:-1])
        if head in occupied:
            return self._finish(StepResult.SELF_COLLISION)

        self.snake.insert(0, head)
        if will_grow:
            self.score += 1
            self._place_food()
            self.last_result = StepResult.ATE_FOOD
        else:
            self.snake.pop()
            self.last_result = StepResult.OK

        return self.last_result

    def _finish(self, result: StepResult) -> StepResult:
        self.game_over = True
        self.last_result = result
        return result

    def _place_food(self) -> None:
        occupied = set(self.snake) | self.obstacles
        for y in range(self.height):
            for x in range(self.width):
                candidate = Point(x, y)
                if candidate not in occupied:
                    self.food = candidate
                    return


def is_valid_move(move: Direction) -> bool:
    return isinstance(move, Direction)

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulator" / "python"))

from autosnake_sim import Direction, GameEngine, Point, StepResult


def test_snake_moves_correctly():
    game = GameEngine()

    result = game.step(Direction.RIGHT)

    assert result == StepResult.OK
    assert game.snake[0] == Point(9, 8)
    assert len(game.snake) == 3


def test_wall_collision_is_detected():
    game = GameEngine(snake=[Point(15, 0), Point(14, 0)], food=Point(1, 1), direction=Direction.RIGHT)

    result = game.step(Direction.RIGHT)

    assert result == StepResult.WALL_COLLISION
    assert game.game_over is True


def test_self_collision_is_detected():
    game = GameEngine(
        snake=[Point(5, 5), Point(5, 6), Point(4, 6), Point(4, 5), Point(4, 4), Point(5, 4)],
        food=Point(10, 10),
        direction=Direction.UP,
    )

    result = game.step(Direction.LEFT)

    assert result == StepResult.SELF_COLLISION
    assert game.game_over is True


def test_food_increases_length_and_score():
    game = GameEngine(snake=[Point(8, 8), Point(7, 8), Point(6, 8)], food=Point(9, 8))

    result = game.step(Direction.RIGHT)

    assert result == StepResult.ATE_FOOD
    assert game.score == 1
    assert len(game.snake) == 4


def test_obstacle_collision_is_detected():
    game = GameEngine(
        snake=[Point(8, 8), Point(7, 8), Point(6, 8)],
        food=Point(12, 8),
        obstacles={Point(9, 8)},
    )

    result = game.step(Direction.RIGHT)

    assert result == StepResult.OBSTACLE_COLLISION
    assert game.game_over is True

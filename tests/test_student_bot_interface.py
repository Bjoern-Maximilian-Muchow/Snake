import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulator" / "python"))

import student_bot
from autosnake_sim import Direction, GameEngine, Point, is_valid_move


def test_student_bot_exposes_choose_move():
    signature = inspect.signature(student_bot.choose_move)

    assert list(signature.parameters) == ["snapshot"]


def test_student_bot_returns_direction():
    game = GameEngine()

    move = student_bot.choose_move(game.snapshot())

    assert is_valid_move(move)


def test_student_bot_returns_valid_move_with_obstacle():
    game = GameEngine(
        snake=[Point(1, 0), Point(1, 1), Point(0, 1)],
        food=Point(3, 0),
        obstacles={Point(2, 0)},
        direction=Direction.UP,
    )

    move = student_bot.choose_move(game.snapshot())

    assert move in game.valid_moves()

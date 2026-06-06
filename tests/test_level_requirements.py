import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulator" / "python"))

from autosnake_sim import Direction, GameEngine, Point, StepResult
from example_bots import basic_rule_bot, bfs_bot, safe_rule_bot


def test_level_schueler_basic_rules_avoid_simple_wall():
    game = GameEngine(snake=[Point(15, 8), Point(14, 8), Point(13, 8)], food=Point(15, 4), direction=Direction.RIGHT)

    move = basic_rule_bot(game.snapshot())

    assert move == Direction.UP


def test_level_student_safe_move_validation():
    game = GameEngine(
        snake=[Point(1, 0), Point(1, 1), Point(0, 1)],
        food=Point(3, 0),
        obstacles={Point(2, 0)},
        direction=Direction.UP,
    )

    move = safe_rule_bot(game.snapshot())
    valid_moves = game.valid_moves()
    result = game.step(move)

    assert move in valid_moves
    assert result != StepResult.WALL_COLLISION
    assert result != StepResult.OBSTACLE_COLLISION


def test_level_advanced_bfs_has_bounded_decision_and_valid_move():
    game = GameEngine(
        snake=[Point(2, 2), Point(2, 3), Point(1, 3), Point(1, 2)],
        food=Point(6, 2),
        obstacles={Point(3, 2), Point(3, 3), Point(4, 3)},
        direction=Direction.RIGHT,
    )

    move = bfs_bot(game.snapshot(), time_limit_ms=5.0)

    assert move in game.valid_moves()

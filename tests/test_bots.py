import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "simulator" / "python"))

from autosnake_sim import Direction, GameEngine, is_valid_move
from example_bots import basic_rule_bot, bfs_bot, safe_rule_bot


def test_basic_bot_returns_valid_move():
    game = GameEngine()

    move = basic_rule_bot(game.snapshot())

    assert is_valid_move(move)
    assert move in Direction


def test_safe_bot_returns_valid_move():
    game = GameEngine()

    move = safe_rule_bot(game.snapshot())

    assert is_valid_move(move)
    assert move in game.valid_moves()


def test_bfs_bot_returns_valid_move():
    game = GameEngine()

    move = bfs_bot(game.snapshot())

    assert is_valid_move(move)
    assert move in game.valid_moves()

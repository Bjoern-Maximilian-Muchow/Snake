from __future__ import annotations

import sys
from pathlib import Path

LEVEL_DIR = Path(__file__).resolve().parent
SIMULATOR_DIR = LEVEL_DIR.parents[1] / "simulator" / "python"
sys.path.insert(0, str(SIMULATOR_DIR))
sys.path.insert(0, str(LEVEL_DIR))

from autosnake_sim import BotSnapshot, Direction, Point
from student_bot import choose_move, is_blocked, safe_moves


def snapshot_with_obstacle() -> BotSnapshot:
    return BotSnapshot(
        head=Point(1, 1),
        food=Point(3, 1),
        direction=Direction.RIGHT,
        snake=(Point(1, 1), Point(0, 1)),
        obstacles=(Point(2, 1),),
        score=0,
    )


def test_is_blocked_erkennt_rand_koerper_und_hindernis():
    snapshot = snapshot_with_obstacle()

    assert is_blocked(snapshot, Point(-1, 1))
    assert is_blocked(snapshot, Point(0, 1))
    assert is_blocked(snapshot, Point(2, 1))
    assert not is_blocked(snapshot, Point(1, 0))


def test_safe_moves_enthaelt_keine_blockierten_zuege():
    moves = safe_moves(snapshot_with_obstacle())

    assert Direction.RIGHT not in moves
    assert Direction.LEFT not in moves
    assert Direction.UP in moves
    assert Direction.DOWN in moves


def test_choose_move_liefert_einen_sicheren_zug():
    snapshot = snapshot_with_obstacle()

    assert choose_move(snapshot) in safe_moves(snapshot)

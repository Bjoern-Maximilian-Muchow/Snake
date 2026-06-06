from __future__ import annotations

from autosnake_sim import DELTAS, BotSnapshot, Direction, OPPOSITES, Point


def choose_move(snapshot: BotSnapshot) -> Direction:
    """Einstiegspunkt fuer eigene Bots.

    Lernende duerfen die Logik in dieser Funktion ersetzen. Die Funktion muss
    immer eine `Direction` zurueckgeben und darf den uebergebenen Spielzustand
    nicht veraendern.
    """
    for move in _food_first_moves(snapshot):
        if _is_safe(snapshot, move):
            return move
    return snapshot.direction


def _food_first_moves(snapshot: BotSnapshot) -> list[Direction]:
    moves: list[Direction] = []
    if snapshot.food.x > snapshot.head.x:
        moves.append(Direction.RIGHT)
    if snapshot.food.x < snapshot.head.x:
        moves.append(Direction.LEFT)
    if snapshot.food.y > snapshot.head.y:
        moves.append(Direction.DOWN)
    if snapshot.food.y < snapshot.head.y:
        moves.append(Direction.UP)
    moves.extend([Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT])
    return list(dict.fromkeys(moves))


def _is_safe(snapshot: BotSnapshot, move: Direction) -> bool:
    if move == OPPOSITES[snapshot.direction]:
        return False

    dx, dy = DELTAS[move]
    next_head = Point(snapshot.head.x + dx, snapshot.head.y + dy)
    blocked = set(snapshot.snake[:-1]) | set(snapshot.obstacles)
    return 0 <= next_head.x < 16 and 0 <= next_head.y < 16 and next_head not in blocked

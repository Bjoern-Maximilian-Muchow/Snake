from __future__ import annotations

from collections import deque
from time import perf_counter

from autosnake_sim import DELTAS, Direction, Point, BotSnapshot, OPPOSITES


def basic_rule_bot(snapshot: BotSnapshot) -> Direction:
    preferred: list[Direction] = []
    if snapshot.food.x > snapshot.head.x:
        preferred.append(Direction.RIGHT)
    if snapshot.food.x < snapshot.head.x:
        preferred.append(Direction.LEFT)
    if snapshot.food.y > snapshot.head.y:
        preferred.append(Direction.DOWN)
    if snapshot.food.y < snapshot.head.y:
        preferred.append(Direction.UP)
    preferred.append(snapshot.direction)

    for move in preferred:
        if move != OPPOSITES[snapshot.direction]:
            return move
    return snapshot.direction


def safe_rule_bot(snapshot: BotSnapshot, width: int = 16, height: int = 16) -> Direction:
    for move in _food_first_moves(snapshot):
        if _is_safe(snapshot, move, width, height):
            return move
    return snapshot.direction


def bfs_bot(snapshot: BotSnapshot, width: int = 16, height: int = 16, time_limit_ms: float = 5.0) -> Direction:
    deadline = perf_counter() + time_limit_ms / 1000.0
    blocked = set(snapshot.snake[:-1])
    queue: deque[tuple[Point, list[Direction]]] = deque([(snapshot.head, [])])
    seen = {snapshot.head}

    while queue and perf_counter() < deadline:
        point, path = queue.popleft()
        if point == snapshot.food and path:
            first = path[0]
            if first != OPPOSITES[snapshot.direction]:
                return first

        for move in Direction:
            if not path and move == OPPOSITES[snapshot.direction]:
                continue
            dx, dy = DELTAS[move]
            nxt = Point(point.x + dx, point.y + dy)
            if (
                0 <= nxt.x < width
                and 0 <= nxt.y < height
                and nxt not in blocked
                and nxt not in seen
            ):
                seen.add(nxt)
                queue.append((nxt, path + [move]))

    return safe_rule_bot(snapshot, width, height)


def _food_first_moves(snapshot: BotSnapshot) -> list[Direction]:
    moves: list[Direction] = []
    horizontal = Direction.RIGHT if snapshot.food.x > snapshot.head.x else Direction.LEFT
    vertical = Direction.DOWN if snapshot.food.y > snapshot.head.y else Direction.UP

    if snapshot.food.x != snapshot.head.x:
        moves.append(horizontal)
    if snapshot.food.y != snapshot.head.y:
        moves.append(vertical)
    moves.extend([Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT])
    return list(dict.fromkeys(moves))


def _is_safe(snapshot: BotSnapshot, move: Direction, width: int, height: int) -> bool:
    if move == OPPOSITES[snapshot.direction]:
        return False
    dx, dy = DELTAS[move]
    nxt = Point(snapshot.head.x + dx, snapshot.head.y + dy)
    body_without_tail = set(snapshot.snake[:-1])
    return 0 <= nxt.x < width and 0 <= nxt.y < height and nxt not in body_without_tail

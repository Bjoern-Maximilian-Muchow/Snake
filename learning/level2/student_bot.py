from __future__ import annotations

from autosnake_sim import BotSnapshot, Direction, Point


def is_blocked(snapshot: BotSnapshot, point: Point) -> bool:
    """Gibt True zurück, wenn das Feld nicht betreten werden darf."""
    # TODO: Rand, Snake-Körper und Hindernisse prüfen.
    return False


def safe_moves(snapshot: BotSnapshot) -> list[Direction]:
    """Ermittelt alle erlaubten und sicheren nächsten Richtungen."""
    # TODO: Alle vier Richtungen untersuchen.
    return []


def choose_move(snapshot: BotSnapshot) -> Direction:
    """Wählt einen sicheren Zug und berücksichtigt möglichst das Futter."""
    # TODO: safe_moves verwenden und eine begründete Priorität festlegen.
    return snapshot.direction

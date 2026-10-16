"""Adapters for the original coursework function contract."""

from .model import Board, Gameboard, Move
from .rules import get_legal_moves
from .search import SearchConfig, search

__all__ = ["get_legal_moves", "studentAgent"]


def studentAgent(gameboard: Gameboard | Board) -> Move:
    """Return white's depth-five move, or the historical no-move sentinel."""
    return search(gameboard, config=SearchConfig(depth=5)).move or ((0, 0), (0, 0))

"""A dependency-free fairy-chess adversarial search engine."""

from .model import Board, Color, Gameboard, Move, Piece, Position
from .rules import get_legal_moves
from .search import SearchConfig, SearchLimitExceeded, SearchResult, SearchStats, search

__all__ = [
    "Board",
    "Color",
    "Gameboard",
    "Move",
    "Piece",
    "Position",
    "SearchConfig",
    "SearchLimitExceeded",
    "SearchResult",
    "SearchStats",
    "get_legal_moves",
    "search",
]

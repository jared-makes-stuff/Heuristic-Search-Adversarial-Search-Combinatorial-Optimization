"""Validated board state and reversible transitions for the fairy-chess variant."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Literal, TypeAlias, cast

Color: TypeAlias = Literal["white", "black"]
Position: TypeAlias = tuple[int, int]
Move: TypeAlias = tuple[Position, Position]
Gameboard: TypeAlias = Iterable[tuple[str, str, Position]]

BOARD_SIZE = 8
WIN_SCORE = 10_000_000
PIECE_VALUES: Mapping[str, int] = MappingProxyType(
    {"King": 10_000, "Rook": 50, "Bishop": 30, "Knight": 30, "Squire": 30, "Combatant": 20}
)


def validate_color(color: str) -> Color:
    if color not in ("white", "black"):
        raise ValueError("color must be 'white' or 'black'")
    return cast(Color, color)


def opponent(color: Color) -> Color:
    return "black" if color == "white" else "white"


def validate_position(position: object) -> Position:
    if (
        not isinstance(position, (tuple, list))
        or len(position) != 2
        or any(type(value) is not int or not 0 <= value < BOARD_SIZE for value in position)
    ):
        raise ValueError("position must contain two integers between 0 and 7")
    return position[0], position[1]


@dataclass(frozen=True, slots=True)
class Piece:
    name: str
    color: Color


@dataclass(frozen=True, slots=True)
class _Undo:
    move: Move
    piece: Piece
    captured: Piece | None


class Board:
    """Own piece placement, king locations, and incremental material balance.

    Mutations are internal to search; callers receive a read-only placement view.
    A board may contain one missing king to represent a terminal position.
    """

    def __init__(self, gameboard: Gameboard):
        if not isinstance(gameboard, Iterable) or isinstance(gameboard, (str, bytes, Mapping)):
            raise ValueError("gameboard must be an iterable of pieces")
        self._pieces: dict[Position, Piece] = {}
        self._kings: dict[Color, Position | None] = {"white": None, "black": None}
        self._material = 0
        for entry in gameboard:
            if not isinstance(entry, (tuple, list)) or len(entry) != 3:
                raise ValueError("each piece must be [name, color, [row, column]]")
            name, raw_color, raw_position = entry
            if not isinstance(name, str) or name not in PIECE_VALUES:
                raise ValueError(f"unknown piece: {name!r}")
            color = validate_color(raw_color)
            position = validate_position(raw_position)
            if position in self._pieces:
                raise ValueError(f"multiple pieces at {position}")
            if name == "King":
                if self._kings[color] is not None:
                    raise ValueError(f"multiple {color} kings")
                self._kings[color] = position
            self._pieces[position] = Piece(name, color)
            self._material += PIECE_VALUES[name] * (1 if color == "white" else -1)
        if all(position is None for position in self._kings.values()):
            raise ValueError("board must contain at least one king")

    @property
    def pieces(self) -> Mapping[Position, Piece]:
        return MappingProxyType(self._pieces)

    @property
    def material(self) -> int:
        return self._material

    def to_gameboard(self) -> list[tuple[str, str, Position]]:
        return [(piece.name, piece.color, pos) for pos, piece in sorted(self._pieces.items())]

    def terminal_score(self, ply: int = 0) -> int | None:
        """Return white's terminal utility, or None while the game continues."""
        if self._kings["white"] is None:
            return -WIN_SCORE + ply
        if self._kings["black"] is None:
            return WIN_SCORE - ply
        if len(self._pieces) == 2:
            return 0
        return None

    def _push(self, move: Move) -> _Undo:
        """Apply a generated legal move. Pair with _pop in a finally block."""
        start, end = move
        piece = self._pieces.pop(start)
        captured = self._pieces.get(end)
        self._pieces[end] = piece
        if piece.name == "King":
            self._kings[piece.color] = end
        if captured is not None:
            self._material -= PIECE_VALUES[captured.name] * (1 if captured.color == "white" else -1)
            if captured.name == "King":
                self._kings[captured.color] = None
        return _Undo(move, piece, captured)

    def _pop(self, undo: _Undo) -> None:
        start, end = undo.move
        del self._pieces[end]
        self._pieces[start] = undo.piece
        if undo.piece.name == "King":
            self._kings[undo.piece.color] = start
        if undo.captured is not None:
            captured = undo.captured
            self._pieces[end] = captured
            self._material += PIECE_VALUES[captured.name] * (1 if captured.color == "white" else -1)
            if captured.name == "King":
                self._kings[captured.color] = end

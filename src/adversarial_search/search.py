"""Instrumented fixed-depth minimax and alpha-beta search."""

from dataclasses import dataclass
from math import inf
from time import perf_counter
from typing import Literal

from .model import Board, Color, Gameboard, Move, opponent, validate_color
from .rules import legal_moves, ordered_moves


@dataclass(frozen=True, slots=True)
class SearchConfig:
    depth: int = 4
    algorithm: Literal["alpha-beta", "minimax"] = "alpha-beta"
    order_moves: bool = True
    node_limit: int | None = None

    def __post_init__(self) -> None:
        if type(self.depth) is not int or not 1 <= self.depth <= 64:
            raise ValueError("depth must be an integer between 1 and 64")
        if self.algorithm not in ("alpha-beta", "minimax"):
            raise ValueError("algorithm must be 'alpha-beta' or 'minimax'")
        if type(self.order_moves) is not bool:
            raise ValueError("order_moves must be a boolean")
        if self.node_limit is not None and (
            type(self.node_limit) is not int or self.node_limit < 1
        ):
            raise ValueError("node_limit must be a positive integer")


class SearchLimitExceeded(RuntimeError):
    """The node budget was exhausted; no complete result is available."""


@dataclass(frozen=True, slots=True)
class SearchStats:
    nodes: int
    leaves: int
    cutoffs: int
    elapsed_seconds: float

    @property
    def nodes_per_second(self) -> float:
        return self.nodes / self.elapsed_seconds if self.elapsed_seconds else 0.0


@dataclass(frozen=True, slots=True)
class SearchResult:
    move: Move | None
    score: int
    depth: int
    stats: SearchStats


def search(
    gameboard: Gameboard | Board,
    color: Color = "white",
    config: SearchConfig | None = None,
) -> SearchResult:
    """Search to the requested ply depth, returning utility from white's view.

    Every transition is restored even when recursion raises. Concurrent searches
    should use separate Board instances (or independent tuple/list inputs).
    """
    validate_color(color)
    config = config or SearchConfig()
    board = gameboard if isinstance(gameboard, Board) else Board(gameboard)
    nodes = leaves = cutoffs = 0
    pruning = config.algorithm == "alpha-beta"
    started = perf_counter()

    def visit(
        side: Color, remaining: int, ply: int, alpha: float, beta: float
    ) -> tuple[int, Move | None]:
        nonlocal nodes, leaves, cutoffs
        if config.node_limit is not None and nodes >= config.node_limit:
            raise SearchLimitExceeded(f"search exceeded node limit of {config.node_limit}")
        nodes += 1
        terminal = board.terminal_score(ply)
        if terminal is not None or remaining == 0:
            leaves += 1
            return (terminal if terminal is not None else board.material), None
        moves = legal_moves(board, side)
        if not moves:
            leaves += 1
            return board.material, None
        if config.order_moves:
            moves = ordered_moves(board, moves)
        best_score = -inf if side == "white" else inf
        best_move = None
        for move in moves:
            undo = board._push(move)
            try:
                score, _ = visit(opponent(side), remaining - 1, ply + 1, alpha, beta)
            finally:
                board._pop(undo)
            if (side == "white" and score > best_score) or (side == "black" and score < best_score):
                best_score, best_move = score, move
            if pruning:
                if side == "white":
                    alpha = max(alpha, best_score)
                else:
                    beta = min(beta, best_score)
                if alpha >= beta:
                    cutoffs += 1
                    break
        return int(best_score), best_move

    score, move = visit(color, config.depth, 0, -inf, inf)
    stats = SearchStats(nodes, leaves, cutoffs, perf_counter() - started)
    return SearchResult(move, score, config.depth, stats)

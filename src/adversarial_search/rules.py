"""Deterministic movement rules, independent of search and evaluation."""

from .model import BOARD_SIZE, PIECE_VALUES, Board, Color, Gameboard, Move, validate_color

ORTHOGONAL = ((-1, 0), (0, -1), (0, 1), (1, 0))
DIAGONAL = ((-1, -1), (-1, 1), (1, -1), (1, 1))
JUMPS = {
    "King": ORTHOGONAL + DIAGONAL,
    "Knight": ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)),
    "Squire": ((-2, 0), (-1, -1), (-1, 1), (0, -2), (0, 2), (1, -1), (1, 1), (2, 0)),
}


def legal_moves(board: Board, color: Color) -> list[Move]:
    validate_color(color)
    if board.terminal_score() is not None:
        return []
    moves: list[Move] = []
    for start, piece in board._pieces.items():
        if piece.color != color:
            continue
        row, col = start
        sliding = piece.name in ("Rook", "Bishop")
        if sliding:
            directions = ORTHOGONAL if piece.name == "Rook" else DIAGONAL
        elif piece.name == "Combatant":
            directions = ORTHOGONAL + DIAGONAL
        else:
            directions = JUMPS[piece.name]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            while 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE:
                end = (nr, nc)
                occupant = board._pieces.get(end)
                if piece.name == "Combatant":
                    if (dr == 0 or dc == 0) and occupant is None:
                        moves.append((start, end))
                    elif dr != 0 and dc != 0 and occupant is not None and occupant.color != color:
                        moves.append((start, end))
                elif occupant is None or occupant.color != color:
                    moves.append((start, end))
                if not sliding or occupant is not None:
                    break
                nr, nc = nr + dr, nc + dc
    return sorted(moves)


def get_legal_moves(gameboard: Gameboard | Board, color: Color) -> list[Move]:
    """Accept either the tuple/list input format or an existing Board."""
    return legal_moves(gameboard if isinstance(gameboard, Board) else Board(gameboard), color)


def ordered_moves(board: Board, moves: list[Move]) -> list[Move]:
    """Try king captures, then valuable captures; retain canonical order on ties."""

    def priority(move: Move) -> tuple[int, int]:
        captured = board._pieces.get(move[1])
        if captured is None:
            return 0, 0
        if captured.name == "King":
            return 2, 0
        return 1, 10 * PIECE_VALUES[captured.name] - PIECE_VALUES[board._pieces[move[0]].name]

    return sorted(moves, key=priority, reverse=True)

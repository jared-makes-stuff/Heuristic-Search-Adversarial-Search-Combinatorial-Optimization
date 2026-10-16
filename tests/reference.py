"""Copy-on-move minimax oracle, independent of the engine's mutable state/search."""

from adversarial_search import get_legal_moves

VALUES = {"King": 10_000, "Rook": 50, "Bishop": 30, "Knight": 30, "Squire": 30, "Combatant": 20}
WIN = 10_000_000


def apply_copy(position, move):
    start, end = move
    result = [(name, color, pos) for name, color, pos in position if pos not in move]
    name, color, _ = next(piece for piece in position if piece[2] == start)
    result.append((name, color, end))
    return result


def minimax(position, color, depth, ply=0):
    kings = {color for name, color, _ in position if name == "King"}
    if "white" not in kings:
        return -WIN + ply
    if "black" not in kings:
        return WIN - ply
    if len(position) == 2:
        return 0
    material = sum(VALUES[name] * (1 if side == "white" else -1) for name, side, _ in position)
    if depth == 0:
        return material
    moves = get_legal_moves(position, color)
    if not moves:
        return material
    next_color = "black" if color == "white" else "white"
    scores = [minimax(apply_copy(position, move), next_color, depth - 1, ply + 1) for move in moves]
    return (max if color == "white" else min)(scores)

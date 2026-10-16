import unittest

from adversarial_search import Board, get_legal_moves
from adversarial_search.model import PIECE_VALUES

KINGS = [("King", "white", (7, 0)), ("King", "black", (0, 7))]


class MovementTests(unittest.TestCase):
    def destinations(self, name, position=(3, 3), others=(), color="white"):
        board = KINGS + [(name, color, position)] + list(others)
        return {end for start, end in get_legal_moves(board, color) if start == position}

    def test_original_move_sample(self):
        position = KINGS + [("Knight", "white", (3, 4))]
        expected = {
            ((7, 0), (7, 1)),
            ((7, 0), (6, 0)),
            ((7, 0), (6, 1)),
            ((3, 4), (5, 5)),
            ((3, 4), (4, 6)),
            ((3, 4), (1, 5)),
            ((3, 4), (2, 6)),
            ((3, 4), (5, 3)),
            ((3, 4), (4, 2)),
            ((3, 4), (1, 3)),
            ((3, 4), (2, 2)),
        }
        self.assertEqual(set(get_legal_moves(position, "white")), expected)

    def test_king_moves_one_square_in_every_direction(self):
        board = [("King", "white", (3, 3)), ("King", "black", (0, 7)), ("Rook", "black", (0, 0))]
        expected = {(r, c) for r in range(2, 5) for c in range(2, 5)} - {(3, 3)}
        self.assertEqual({end for start, end in get_legal_moves(board, "white")}, expected)

    def test_knight_jumps_over_blockers(self):
        blockers = [
            ("Combatant", "white", (r, c))
            for r in range(2, 5)
            for c in range(2, 5)
            if (r, c) != (3, 3)
        ]
        expected = {(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)}
        self.assertEqual(self.destinations("Knight", others=blockers), expected)

    def test_squire_jumps_manhattan_distance_two(self):
        expected = {(1, 3), (2, 2), (2, 4), (3, 1), (3, 5), (4, 2), (4, 4), (5, 3)}
        self.assertEqual(
            self.destinations("Squire", others=[("Combatant", "white", (3, 4))]), expected
        )

    def test_rook_stops_at_blockers_and_captures_enemy(self):
        others = [("Combatant", "white", (3, 5)), ("Combatant", "black", (1, 3))]
        expected = {(3, 0), (3, 1), (3, 2), (3, 4), (2, 3), (1, 3), (4, 3), (5, 3), (6, 3), (7, 3)}
        self.assertEqual(self.destinations("Rook", others=others), expected)

    def test_bishop_stops_at_blockers_and_captures_enemy(self):
        others = [("Combatant", "white", (1, 1)), ("Combatant", "black", (5, 5))]
        expected = {(2, 2), (2, 4), (1, 5), (0, 6), (4, 2), (5, 1), (6, 0), (4, 4), (5, 5)}
        self.assertEqual(self.destinations("Bishop", others=others), expected)

    def test_combatant_separates_capture_and_quiet_rules(self):
        others = [
            ("Rook", "black", (3, 4)),
            ("Rook", "black", (4, 4)),
            ("Rook", "white", (2, 2)),
            ("Rook", "white", (3, 2)),
        ]
        self.assertEqual(self.destinations("Combatant", others=others), {(2, 3), (4, 3), (4, 4)})

    def test_friendly_destination_rejected_for_jumping_pieces(self):
        for name, target in (("Knight", (5, 4)), ("Squire", (5, 3))):
            with self.subTest(piece=name):
                self.assertNotIn(
                    target, self.destinations(name, others=[("Rook", "white", target)])
                )

    def test_edges_never_wrap(self):
        counts = {"Rook": 14, "Bishop": 7, "Knight": 2, "Squire": 3, "Combatant": 2}
        for name, count in counts.items():
            with self.subTest(piece=name):
                board = [
                    ("King", "white", (6, 5)),
                    ("King", "black", (5, 7)),
                    (name, "white", (0, 0)),
                ]
                moves = [end for start, end in get_legal_moves(board, "white") if start == (0, 0)]
                self.assertEqual(len(moves), count)
                self.assertTrue(all(0 <= r < 8 and 0 <= c < 8 for r, c in moves))

    def test_both_colors_share_movement_rules(self):
        for name in ("Knight", "Squire", "Combatant", "Rook", "Bishop"):
            with self.subTest(piece=name):
                self.assertEqual(self.destinations(name), self.destinations(name, color="black"))

    def test_king_safety_is_not_standard_chess(self):
        board = KINGS + [("Rook", "black", (6, 7))]
        self.assertIn(((7, 0), (6, 0)), get_legal_moves(board, "white"))

    def test_king_only_draw_overrides_adjacent_capture(self):
        board = [("King", "white", (0, 0)), ("King", "black", (0, 1))]
        self.assertEqual(Board(board).terminal_score(), 0)
        self.assertEqual(get_legal_moves(board, "white"), [])
        self.assertEqual(get_legal_moves(board, "black"), [])

    def test_missing_king_ends_play(self):
        self.assertEqual(get_legal_moves([("King", "white", (0, 0))], "white"), [])


class BoardTests(unittest.TestCase):
    def test_invalid_boards_fail_explicitly(self):
        invalid = [
            None,
            3,
            "invalid",
            {},
            [],
            [("Queen", "white", (3, 3))] + KINGS,
            [("Rook", "blue", (3, 3))] + KINGS,
            [("Rook", "white", (-1, 3))] + KINGS,
            [("Rook", "white", (8, 3))] + KINGS,
            [("Rook", "white", (True, 3))] + KINGS,
            [("Rook", "white", (3.0, 3))] + KINGS,
            [("Rook", "white", (3,))] + KINGS,
            [("Rook", "white", "33")] + KINGS,
            [("Rook", "white", (7, 0))] + KINGS,
            [("King", "white", (3, 3))] + KINGS,
            [("Rook", "white", (3, 3))],
            [("King", "white")],
            [None],
        ]
        for board in invalid:
            with self.subTest(board=board), self.assertRaises(ValueError):
                Board(board)

    def test_invalid_player_rejected(self):
        with self.assertRaises(ValueError):
            get_legal_moves(KINGS, "blue")

    def test_board_owns_input_and_exposes_immutable_pieces(self):
        raw = [["King", "white", [0, 0]], ["King", "black", [7, 7]]]
        board = Board(raw)
        raw[0][2][0] = 5
        self.assertIn((0, 0), board.pieces)
        with self.assertRaises(TypeError):
            board.pieces[(0, 0)] = None
        with self.assertRaises(AttributeError):
            board.pieces[(0, 0)].name = "Rook"

    def test_every_move_round_trips_captures_material_and_kings(self):
        position = KINGS + [("Rook", "white", (2, 7)), ("Combatant", "black", (2, 4))]
        board = Board(position)
        before = board.to_gameboard(), board.material, board.terminal_score()
        for color in ("white", "black"):
            for move in get_legal_moves(board, color):
                with self.subTest(move=move):
                    undo = board._push(move)
                    fresh = Board(board.to_gameboard())
                    self.assertEqual(board.material, fresh.material)
                    self.assertEqual(board.terminal_score(), fresh.terminal_score())
                    board._pop(undo)
                    self.assertEqual(
                        (board.to_gameboard(), board.material, board.terminal_score()), before
                    )

    def test_material_is_white_minus_black(self):
        board = Board(KINGS + [("Rook", "white", (3, 3)), ("Knight", "black", (4, 4))])
        self.assertEqual(board.material, PIECE_VALUES["Rook"] - PIECE_VALUES["Knight"])

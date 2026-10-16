import random
import unittest
from unittest.mock import patch

import AB
import AB_solution
from adversarial_search import Board, SearchConfig, SearchLimitExceeded, get_legal_moves, search
from adversarial_search.model import WIN_SCORE
from adversarial_search.positions import DEMO, ENDGAME, MIDGAME, TACTICAL
from tests import fixtures
from tests.reference import apply_copy, minimax


class SearchTests(unittest.TestCase):
    def test_original_immediate_king_capture(self):
        for module in (AB, AB_solution):
            with self.subTest(module=module.__name__):
                self.assertEqual(module.studentAgent(DEMO), ((3, 4), (4, 6)))
                self.assertEqual(
                    module.get_legal_moves(DEMO, "white"), get_legal_moves(DEMO, "white")
                )
        result = search(DEMO)
        self.assertEqual(result.score, WIN_SCORE - 1)

    def test_black_minimizes_and_captures_white_king(self):
        position = [
            (name, "black" if color == "white" else "white", pos) for name, color, pos in DEMO
        ]
        result = search(position, "black")
        self.assertEqual(result.move, ((3, 4), (4, 6)))
        self.assertEqual(result.score, -WIN_SCORE + 1)

    def test_terminal_results_have_no_move(self):
        cases = [
            ([("King", "white", (0, 0))], WIN_SCORE),
            ([("King", "black", (0, 0))], -WIN_SCORE),
            ([("King", "white", (0, 0)), ("King", "black", (0, 1))], 0),
        ]
        for position, expected in cases:
            with self.subTest(position=position):
                result = search(position)
                self.assertIsNone(result.move)
                self.assertEqual(result.score, expected)
                self.assertEqual(
                    (result.stats.nodes, result.stats.leaves, result.stats.cutoffs), (1, 1, 0)
                )
                self.assertEqual(AB.studentAgent(position), ((0, 0), (0, 0)))

    def test_nonterminal_no_moves_uses_material(self):
        # A full board blocks all quiet moves. The only diagonal attacker of the
        # black king is a friendly knight, which cannot capture it from (6, 6).
        position = [
            ("King", "white", (0, 0)),
            ("King", "black", (7, 7)),
            ("Knight", "white", (6, 6)),
        ]
        position += [
            ("Combatant", "white", (r, c))
            for r in range(8)
            for c in range(8)
            if (r, c) not in ((0, 0), (7, 7), (6, 6))
        ]
        board = Board(position)
        self.assertIsNone(board.terminal_score())
        self.assertEqual(get_legal_moves(board, "white"), [])
        result = search(board)
        self.assertIsNone(result.move)
        self.assertEqual(result.score, board.material)

    def test_invalid_search_configuration(self):
        for kwargs in (
            {"depth": 0},
            {"depth": -1},
            {"depth": 65},
            {"depth": True},
            {"depth": 2.5},
            {"algorithm": "negamax"},
            {"node_limit": 0},
            {"node_limit": True},
            {"node_limit": 2.5},
            {"order_moves": 1},
        ):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                SearchConfig(**kwargs)
        with self.assertRaises(ValueError):
            search(DEMO, "blue")

    def test_search_restores_board_and_caches(self):
        board = Board(TACTICAL)
        before = board.to_gameboard(), board.material, board.terminal_score()
        result = search(board, config=SearchConfig(depth=3))
        self.assertIn(result.move, get_legal_moves(board, "white"))
        self.assertEqual((board.to_gameboard(), board.material, board.terminal_score()), before)

    def test_node_budget_restores_nested_state_and_returns_no_partial_result(self):
        board = Board(TACTICAL)
        before = board.to_gameboard(), board.material, board.terminal_score()
        with self.assertRaisesRegex(SearchLimitExceeded, "node limit of 10"):
            search(board, config=SearchConfig(depth=5, node_limit=10))
        self.assertEqual((board.to_gameboard(), board.material, board.terminal_score()), before)
        self.assertEqual(
            search(board, config=SearchConfig(depth=2)).score,
            search(TACTICAL, config=SearchConfig(depth=2)).score,
        )
        complete = search(board, config=SearchConfig(depth=2))
        exact_budget = search(board, config=SearchConfig(depth=2, node_limit=complete.stats.nodes))
        self.assertEqual(exact_budget.score, complete.score)
        self.assertEqual(exact_budget.stats.nodes, complete.stats.nodes)

    def test_forced_loss_preserves_terminal_score(self):
        position = [
            ("King", "white", (0, 0)),
            ("King", "black", (7, 7)),
            ("Rook", "black", (0, 2)),
            ("Rook", "black", (2, 0)),
            ("Knight", "black", (3, 2)),
        ]
        result = search(position, config=SearchConfig(depth=2))
        self.assertEqual(result.score, -WIN_SCORE + 2)
        self.assertEqual(result.score, minimax(position, "white", 2))

    def test_unexpected_recursive_error_restores_state(self):
        board = Board(TACTICAL)
        before = board.to_gameboard(), board.material, board.terminal_score()
        calls = 0

        def fail_after_move(current, color):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise RuntimeError("injected evaluator failure")
            return get_legal_moves(current, color)

        with patch("adversarial_search.search.legal_moves", side_effect=fail_after_move):
            with self.assertRaisesRegex(RuntimeError, "injected"):
                search(board)
        self.assertEqual((board.to_gameboard(), board.material, board.terminal_score()), before)

    def test_input_order_does_not_change_result_or_node_counts(self):
        original = search(TACTICAL, config=SearchConfig(depth=3))
        shuffled = list(TACTICAL)
        random.Random(3243).shuffle(shuffled)
        result = search(shuffled, config=SearchConfig(depth=3))
        self.assertEqual(
            (original.move, original.score, original.stats.nodes),
            (result.move, result.score, result.stats.nodes),
        )

    def test_alpha_beta_matches_copy_oracle_for_both_players(self):
        rng = random.Random(3243)
        cases = [DEMO, ENDGAME, TACTICAL]
        for _ in range(8):
            squares = rng.sample([(r, c) for r in range(8) for c in range(8)], 5)
            cases.append(
                [("King", "white", squares[0]), ("King", "black", squares[1])]
                + [
                    (
                        rng.choice(("Squire", "Combatant", "Knight", "Rook", "Bishop")),
                        rng.choice(("white", "black")),
                        pos,
                    )
                    for pos in squares[2:]
                ]
            )
        for position in cases:
            for color in ("white", "black"):
                expected = minimax(position, color, 2)
                for algorithm, ordering in (
                    ("minimax", False),
                    ("alpha-beta", False),
                    ("alpha-beta", True),
                ):
                    with self.subTest(
                        position=position, color=color, algorithm=algorithm, ordering=ordering
                    ):
                        result = search(position, color, SearchConfig(2, algorithm, ordering))
                        self.assertEqual(result.score, expected)
                        child = apply_copy(position, result.move)
                        self.assertEqual(
                            minimax(child, "black" if color == "white" else "white", 1, 1), expected
                        )

    def test_pruning_reduces_nodes_without_changing_value(self):
        plain = search(MIDGAME, config=SearchConfig(3, "minimax", False))
        pruned = search(MIDGAME, config=SearchConfig(3))
        self.assertEqual(plain.score, pruned.score)
        self.assertLess(pruned.stats.nodes, plain.stats.nodes)
        self.assertGreater(pruned.stats.cutoffs, 0)
        self.assertEqual(plain.stats.cutoffs, 0)
        self.assertLessEqual(pruned.stats.leaves, pruned.stats.nodes)

    def test_original_public_tactics_remain_optimal(self):
        cases = [
            (fixtures.public_m1_1, 1, ((1, 7), (1, 5))),
            (fixtures.public_m3_1, 3, ((5, 1), (5, 0))),
            (fixtures.public_m5_1, 5, ((2, 3), (2, 4))),
            (fixtures.public_e3_1, 3, ((2, 2), (2, 4))),
            (fixtures.public_e3_2, 3, ((1, 2), (2, 1))),
        ]
        for position, depth, expected_move in cases:
            with self.subTest(depth=depth, move=expected_move):
                result = search(position, config=SearchConfig(depth))
                self.assertIn(expected_move, get_legal_moves(position, "white"))
                expected_score = minimax(apply_copy(position, expected_move), "black", depth - 1, 1)
                self.assertEqual(result.score, expected_score)
                self.assertEqual(result.score, minimax(position, "white", depth))

    def test_all_original_midgame_fixtures_generate_valid_moves(self):
        for position in (fixtures.b1, fixtures.b2, fixtures.b3, fixtures.b4):
            for color in ("white", "black"):
                with self.subTest(position=position, color=color):
                    moves = get_legal_moves(position, color)
                    result = search(position, color, SearchConfig(1))
                    self.assertIn(result.move, moves)
                    self.assertEqual(len(moves), len(set(moves)))

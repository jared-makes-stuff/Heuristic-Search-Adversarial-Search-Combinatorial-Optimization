import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from adversarial_search.benchmark import run_benchmark


class CliTests(unittest.TestCase):
    def run_cli(self, *args, cwd=None):
        return subprocess.run(
            [sys.executable, "-m", "adversarial_search", *args],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=cwd,
        )

    def test_demo_emits_json(self):
        result = self.run_cli("analyze", "--depth", "2")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["move"], [[3, 4], [4, 6]])
        self.assertEqual(payload["depth"], 2)
        self.assertGreater(payload["stats"]["nodes_per_second"], 0)
        self.assertEqual(result.stderr, "")

    def test_json_file_and_black_player_work_outside_repo(self):
        with tempfile.TemporaryDirectory() as directory:
            position = Path(directory) / "board.json"
            position.write_text(
                json.dumps(
                    [
                        ["King", "black", [0, 0]],
                        ["King", "white", [0, 2]],
                        ["Rook", "black", [1, 2]],
                    ]
                ),
                encoding="utf-8",
            )
            result = self.run_cli(
                "analyze", str(position), "--color", "black", "--depth", "1", cwd=directory
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["move"], [[1, 2], [0, 2]])

    def test_invalid_json_and_board_data_are_clean_errors(self):
        for raw in (
            "{",
            "null",
            "{}",
            '[["Queen", "white", [0, 0]]]',
            '[["King", "white", [true, 0]]]',
            "[null]",
            '[[null, "white", [0, 0]]]',
        ):
            with self.subTest(raw=raw), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "invalid.json"
                path.write_text(raw, encoding="utf-8")
                result = self.run_cli("analyze", str(path))
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_is_clean_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_cli("analyze", str(Path(directory) / "missing.json"))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("Traceback", result.stderr)

    def test_configuration_and_budget_errors_exit_nonzero(self):
        for args in (
            ("--depth", "0"),
            ("--depth", "65"),
            ("--node-limit", "0"),
            ("--node-limit", "1"),
        ):
            with self.subTest(args=args):
                result = self.run_cli("analyze", *args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertNotIn("Traceback", result.stderr)

    def test_terminal_board_emits_null_move(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "terminal.json"
            path.write_text('[["King", "white", [0, 0]]]', encoding="utf-8")
            result = self.run_cli("analyze", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIsNone(json.loads(result.stdout)["move"])

    def test_benchmark_cli_reports_all_variants(self):
        result = self.run_cli("benchmark", "--depth", "1", "--repeats", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload["results"]), 9)
        self.assertTrue(payload["methodology"]["score_agreement"])

    def test_benchmark_validates_repeats_and_node_budget(self):
        for repeats in (0, 101, True):
            with self.subTest(repeats=repeats), self.assertRaises(ValueError):
                run_benchmark(repeats=repeats)
        result = self.run_cli("benchmark", "--node-limit", "1")
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")

    def test_repeated_benchmark_counts_are_reproducible(self):
        payload = run_benchmark(depth=1, repeats=2)
        for name in {row["position"] for row in payload["results"]}:
            rows = [row for row in payload["results"] if row["position"] == name]
            self.assertEqual(len({row["score"] for row in rows}), 1)
            self.assertEqual(rows[0]["node_reduction_percent"], 0)

"""JSON command-line interface. Diagnostics go to stderr; results to stdout."""

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

from .benchmark import run_benchmark
from .positions import DEMO
from .search import SearchConfig, SearchLimitExceeded, search


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic fairy-chess adversarial search")
    subparsers = parser.add_subparsers(dest="command", required=True)
    analyze = subparsers.add_parser("analyze", help="search a position and emit JSON")
    analyze.add_argument(
        "position", nargs="?", type=Path, help="JSON file; defaults to the king-capture demo"
    )
    analyze.add_argument("--color", choices=("white", "black"), default="white")
    analyze.add_argument("--depth", type=int, default=4)
    analyze.add_argument("--algorithm", choices=("alpha-beta", "minimax"), default="alpha-beta")
    analyze.add_argument("--no-ordering", action="store_true")
    analyze.add_argument("--node-limit", type=int, default=1_000_000)
    benchmark = subparsers.add_parser("benchmark", help="compare minimax and alpha-beta; emit JSON")
    benchmark.add_argument("--depth", type=int, default=3)
    benchmark.add_argument("--repeats", type=int, default=3)
    benchmark.add_argument("--node-limit", type=int, default=1_000_000)
    args = parser.parse_args(argv)
    try:
        if args.command == "benchmark":
            payload = run_benchmark(args.depth, args.repeats, args.node_limit)
        else:
            position = DEMO
            if args.position is not None:
                position = json.loads(args.position.read_text(encoding="utf-8"))
                if not isinstance(position, list):
                    raise ValueError("position JSON must be a list of pieces")
            config = SearchConfig(args.depth, args.algorithm, not args.no_ordering, args.node_limit)
            result = search(position, args.color, config)
            payload = asdict(result)
            payload["color"] = args.color
            payload["config"] = asdict(config)
            payload["stats"]["nodes_per_second"] = result.stats.nodes_per_second
        print(json.dumps(payload, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError, SearchLimitExceeded) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

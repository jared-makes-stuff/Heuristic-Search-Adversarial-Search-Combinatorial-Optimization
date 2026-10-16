"""Reproducible score-checked experiments; timing is descriptive, not a gate."""

import platform
from dataclasses import asdict
from datetime import datetime, timezone
from statistics import median

from .positions import WORKLOADS
from .search import SearchConfig, search


def run_benchmark(depth: int = 3, repeats: int = 3, node_limit: int = 1_000_000) -> dict:
    """Compare identical depths/evaluation across three traversal configurations.

    Counts include the root and terminal nodes. Each measured repetition starts
    with a fresh board; one unmeasured warm-up precedes each configuration.
    """
    if type(repeats) is not int or not 1 <= repeats <= 100:
        raise ValueError("repeats must be an integer between 1 and 100")
    variants = (
        ("minimax", "minimax", False),
        ("alpha-beta", "alpha-beta", False),
        ("alpha-beta-ordered", "alpha-beta", True),
    )
    rows = []
    for name, position in WORKLOADS.items():
        reference_score = baseline_nodes = None
        for label, algorithm, ordering in variants:
            config = SearchConfig(depth, algorithm, ordering, node_limit)
            search(position, config=config)
            results = [search(position, config=config) for _ in range(repeats)]
            first = results[0]
            counters = (
                first.move,
                first.score,
                first.stats.nodes,
                first.stats.leaves,
                first.stats.cutoffs,
            )
            for result in results[1:]:
                observed = (
                    result.move,
                    result.score,
                    result.stats.nodes,
                    result.stats.leaves,
                    result.stats.cutoffs,
                )
                if observed != counters:
                    raise RuntimeError(f"nondeterministic search counters for {name}/{label}")
            if reference_score is None:
                reference_score, baseline_nodes = first.score, first.stats.nodes
            elif first.score != reference_score:
                raise RuntimeError(f"minimax score mismatch for {name}/{label}")
            elapsed = median(result.stats.elapsed_seconds for result in results)
            rows.append(
                {
                    "position": name,
                    "variant": label,
                    "depth": depth,
                    "move": first.move,
                    "score": first.score,
                    "nodes": first.stats.nodes,
                    "leaves": first.stats.leaves,
                    "cutoffs": first.stats.cutoffs,
                    "node_reduction_percent": 100 * (1 - first.stats.nodes / baseline_nodes),
                    "median_elapsed_seconds": elapsed,
                    "nodes_per_second": first.stats.nodes / elapsed if elapsed else 0.0,
                    "config": asdict(config),
                }
            )
    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        },
        "methodology": {
            "repeats": repeats,
            "warmups_per_variant": 1,
            "score_perspective": "white",
            "score_agreement": True,
            "timing": "median wall time per search; hardware dependent",
            "baseline": "unpruned minimax without capture ordering",
            "ties": "first move in traversal order; equally valued moves may differ across variants",
        },
        "results": rows,
    }

# Benchmark methodology and local evidence

Run from an installed environment:

```bash
python -m adversarial_search benchmark --depth 3 --repeats 3
```

The command emits JSON with environment metadata, configuration, chosen moves,
scores, nodes, leaves, cutoffs, median elapsed seconds, and nodes per second.
[The reference output](benchmark-results.json) records a local run on
2026-10-16 using CPython 3.14.5 on Windows 11 / AMD64.

## Workloads and controls

Three fixed positions in `src/adversarial_search/positions.py` are derived from
the original public game examples: a five-piece endgame, four-piece tactical
position, and twenty-piece midgame. All variants use the same rules, utility,
terminal handling, and ply depth. Each variant gets one unmeasured warm-up and
three measured repetitions on fresh boards. The elapsed metric starts after
board construction and includes recursive search and move ordering.

The baseline is unpruned minimax in canonical order. The second variant adds
alpha-beta in that same order; the third also prioritizes captures. The harness
rejects score disagreement across variants or inconsistent moves/counters across
repetitions of the same variant. Equally valued root moves can differ between
ordering configurations, so cross-variant agreement is on score.

The default one-million-node budget applies to every search, including warm-ups.
If it is exhausted, the command exits with an error and emits no partial report.
Increasing the depth can make plain minimax expensive.

## Recorded depth-three results

| Position | Variant | Score | Nodes | Fewer nodes vs minimax | Median search time |
| --- | --- | ---: | ---: | ---: | ---: |
| Endgame | Minimax | 20 | 1,436 | baseline | 1.518 ms |
| Endgame | Alpha-beta | 20 | 552 | 61.56% | 0.709 ms |
| Endgame | Ordered alpha-beta | 20 | 402 | 72.01% | 0.700 ms |
| Tactical | Minimax | 0 | 4,048 | baseline | 4.056 ms |
| Tactical | Alpha-beta | 0 | 718 | 82.26% | 0.967 ms |
| Tactical | Ordered alpha-beta | 0 | 319 | 92.12% | 0.758 ms |
| Midgame | Minimax | 30 | 126,990 | baseline | 147.455 ms |
| Midgame | Alpha-beta | 30 | 13,073 | 89.71% | 18.681 ms |
| Midgame | Ordered alpha-beta | 30 | 3,554 | 97.20% | 5.934 ms |

Reduction is `100 × (1 - variant_nodes / minimax_nodes)`. Counts include the
root and terminal nodes. Timings are machine-dependent observations, not latency
guarantees. These small fixed workloads demonstrate pruning mechanics, not
general playing strength, financial performance, or statistically robust speedups.

## Validation scope

The standard-library suite covers the original move sample and five public
tactical positions, all movement rules, input errors, terminal states, no-move
leaves, deterministic ordering, make/unmake restoration, budget exhaustion,
unexpected recursion errors, and CLI subprocesses. A separate copy-on-move
minimax implementation checks fixed-depth scores and selected moves on seeded
positions for both players.

GitHub Actions is configured for Python 3.12–3.14. Remote workflow execution is
not represented by this local evidence. Tests compare node reduction on a fixed
fixture, while timing is intentionally descriptive rather than a pass/fail gate.

Local checks completed on 2026-10-16:

- `python -m unittest discover -s tests -v`: all 41 tests passed with CPython
  3.14.5 using an editable install, and with CPython 3.12.10 using a regular wheel
  installed into a separate environment. The wheel tests include a real CLI
  subprocess with its working directory outside the repository.
- `python -m ruff check .` and `python -m ruff format --check .`: passed with
  Ruff 0.17.1.
- `python -m pip wheel --no-deps .` and isolated wheel installation: succeeded;
  `python -m pip check` reported no broken requirements in both environments.
- All nine reference benchmark scores, node counts, leaf counts, and cutoff
  counts matched a rerun against the final source.

Python 3.13 and Linux are configured in CI but were not tested locally.

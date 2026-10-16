# Portfolio and resume copy

## Project title

**Adversarial Search Engine | Python, Algorithms, Performance Engineering**

## Portfolio description

Built a standalone Python search engine for a six-piece fairy-chess variant,
with deterministic minimax and alpha-beta search, reversible board transitions,
validated inputs, and a JSON CLI. Added regression tests and a reproducible
benchmark harness that checks optimized search against an unpruned baseline.
Ordered alpha-beta explored 3,554 nodes versus 126,990 for minimax on the included
depth-three, twenty-piece midgame, preserving the search value.

## Resume bullet

Engineered a tested Python adversarial-search package with a JSON CLI, reversible
state transitions, and minimax validation; reduced explored nodes by 97.2% using
ordered alpha-beta pruning on a fixed depth-three, twenty-piece benchmark.

For a quant-developer application, emphasize the implemented work: deterministic
simulation, invariants, recursive decision algorithms, instrumentation, and
benchmark controls. The project does not implement a trading strategy, market
simulation, risk model, or financial optimization problem.

## Interview talking points

- **Correctness before speed:** compare values and selected actions to a separate
  copy-on-move minimax oracle, and retain original tactical regression positions.
- **State ownership:** immutable pieces and one authoritative placement map;
  make/unmake preserves king caches and incremental material on success and error.
- **Performance trade-offs:** alpha-beta avoids exploring irrelevant branches,
  while sorting captures costs time. Present node counts alongside observed timing.
- **Resource limits:** fail explicitly on budget exhaustion instead of reporting
  an incomplete root search as optimal.
- **Reproducibility:** fixed positions, canonical traversal, warm-ups, repeated
  measurements, score agreement, and recorded environment metadata.
- **Scope:** fixed-depth material evaluation has a horizon limit; node reductions
  on three positions do not prove general playing strength.

## Evidence and attribution

The source began as a CS3243 fairy-chess adversarial-search project. The original
public game positions are retained as regression fixtures. The standalone package,
CLI, test suite, and benchmark harness extend that starting point. Describe the
work and results accurately when discussing authorship or implementation choices.

Use the [benchmark methodology and raw output](BENCHMARKS.md) to support the
quantified resume bullet. Keep its depth and workload qualifier when shortening it.

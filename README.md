# Adversarial Search Engine

A Python engine for exploring game trees, testing adversarial decisions, and measuring search performance. Built around a six-piece fairy-chess variant, with a reusable API, JSON CLI, and reproducible minimax versus alpha-beta experiments.

**Python 3.12+ · Zero runtime dependencies · 41 automated tests · Minimax baseline**

At depth three on the included 20-piece midgame, ordered alpha-beta visited **3,554 nodes versus 126,990 for minimax: 97.20% fewer nodes**, with the same search value. This is a measured result for a fixed workload; see [methodology and raw results](docs/BENCHMARKS.md).

## Why this project

The engineering focus is correctness and measurable efficiency: validate state at the boundary, restore every simulated move, preserve deterministic results, and compare optimizations against a baseline. These are useful discussion points for software-engineering and quant-developer interviews: recursive algorithms, state invariants, performance instrumentation, and reproducible experiments.

The application is a game-search engine. Its quant-development relevance comes from those engineering skills; the repository contains no market data, pricing model, backtest, or trading strategy.

## Run it

From the repository root, create an isolated environment and install the package.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Then run:

```bash
python -m adversarial_search analyze examples/king_capture.json --depth 3
python -m unittest discover -s tests -v
python -m adversarial_search benchmark --depth 3 --repeats 3
```

For development, install `python -m pip install -e ".[dev]"` and run
`python -m ruff check .` and `python -m ruff format --check .` before contributing.
Ruff is a development dependency; the engine itself uses only the standard library.

The demo selects `((3, 4), (4, 6))`, capturing the black king. Analysis output is JSON containing the move, white-perspective score, depth, node count, leaf count, cutoffs, and elapsed time. The installed `search-engine` command accepts the same arguments.

## Python API

```python
from adversarial_search import SearchConfig, get_legal_moves, search

position = [
    ("King", "white", (7, 0)),
    ("King", "black", (4, 6)),
    ("Knight", "white", (3, 4)),
]

result = search(position, color="white", config=SearchConfig(depth=3))
assert result.move == ((3, 4), (4, 6))
assert result.move in get_legal_moves(position, "white")
print(result.score, result.stats.nodes, result.stats.cutoffs)
```

`SearchConfig` selects depth (1–64 plies), `"alpha-beta"` or `"minimax"`, capture ordering, and an optional node limit. White maximizes; black minimizes. The score always describes white's position. Equal scores keep the first move in traversal order, which is deterministic regardless of input-piece order. Changing capture ordering can select a different equally valued move.

Terminal positions return `move=None`. The CLI defaults to a one-million-node limit; the Python API has no limit unless configured. Exceeding a limit raises `SearchLimitExceeded`, restores the board, and returns no partial result. Invalid board/configuration input raises `ValueError`; CLI input errors produce stderr diagnostics and exit code 2.

## Search and state design

| Component | Responsibility |
| --- | --- |
| [`model.py`](src/adversarial_search/model.py) | Validated board, immutable pieces, cached king locations, incremental material, reversible transitions |
| [`rules.py`](src/adversarial_search/rules.py) | Legal moves, canonical ordering, capture priorities |
| [`search.py`](src/adversarial_search/search.py) | Fixed-depth minimax / alpha-beta, node budget, statistics |
| [`benchmark.py`](src/adversarial_search/benchmark.py) | Fixed workloads, baseline comparisons, repeatability and score checks |
| [`cli.py`](src/adversarial_search/cli.py) | JSON input/output and command-line validation |

Moves update one board in place and undo in `finally` blocks, avoiding a board copy at every search node. Captures update the material balance incrementally. Tests check both piece placement and cached state after normal searches, king captures, budget exhaustion, and injected exceptions. Independent concurrent searches should use separate board instances.

The evaluation uses white-minus-black material: Rook 50, Bishop/Knight/Squire 30, Combatant 20. Terminal wins/losses use ±10,000,000 adjusted by distance from the root, preferring earlier wins and later losses. Scores are heuristic units, not probabilities. A nonterminal position with no legal moves is evaluated as a static leaf.

## Game rules

The board is 8 × 8, with zero-based `(row, column)` coordinates. JSON uses `[piece_name, color, [row, column]]` entries; the Python API also accepts tuples.

| Piece | Movement |
| --- | --- |
| King | One square in any direction |
| Rook | Any distance orthogonally; blocked by pieces |
| Bishop | Any distance diagonally; blocked by pieces |
| Knight | Standard L-shaped jump |
| Squire | Jumps to a square at Manhattan distance two |
| Combatant | Moves one square orthogonally to an empty square; captures one square diagonally |

Capturing a king wins immediately. A position containing only the two kings is an immediate draw, even when they are adjacent. This variant allows moving into attack; check, checkmate, castling, promotion, and en passant do not apply.

## Validation and limitations

The standard-library test suite preserves the original sample and public tactical positions, checks all six movement rules and invalid input, and compares both search variants against a separate copy-on-move minimax oracle on seeded positions for both players. Benchmark timing is descriptive; deterministic search values and node counts support comparisons.

[GitHub Actions](.github/workflows/ci.yml) is configured to install and test the package on Python 3.12, 3.13, and 3.14, including CLI and benchmark smoke checks. Local validation is recorded in [the benchmark notes](docs/BENCHMARKS.md); remote CI results depend on running that workflow.

Search is single-threaded and fixed-depth. There is no transposition table, quiescence search, iterative deepening, repetition rule, or playing-strength rating. Material evaluation can miss tactics beyond its horizon. Node reduction on the supplied positions does not establish general speed or playing strength.

## Portfolio use and provenance

Suggested project title: **Adversarial Search Engine | Python, Algorithms, Performance Engineering**.

Suggested resume bullet:

> Engineered a tested Python adversarial-search package with a JSON CLI, reversible state transitions, and minimax validation; reduced explored nodes by 97.2% using ordered alpha-beta pruning on a fixed depth-three, 20-piece benchmark.

See [portfolio wording and interview talking points](docs/PORTFOLIO.md), [architecture](docs/ARCHITECTURE.md), and [project requirements](docs/PRD.md).

The project began as a CS3243 fairy-chess adversarial-search implementation and was restructured as a standalone engineering project. Public sample positions remain as regression fixtures. The supplied assignment PDF and extracted scratch text have been removed. The original `studentAgent(gameboard)` and `get_legal_moves(gameboard, color)` imports remain available through `AB` and `AB_solution` after installation; both delegate to the package. The old template's internal classes and `ab` helper are superseded by the documented package API.

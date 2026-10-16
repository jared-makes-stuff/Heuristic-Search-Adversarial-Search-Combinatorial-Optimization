# Adversarial Search Engine

## Problem and audience

Turn an existing fairy-chess alpha-beta implementation into a reproducible Python
project that a software-engineering or quant-developer interviewer can run,
inspect, and discuss. Preserve the game and its coursework provenance. The
project demonstrates algorithm engineering; it makes no trading or finance-model claims.

## Requirements

1. One typed implementation separates validated board state, movement rules,
   evaluation, search, and command-line input/output. No runtime dependencies.
2. Support white and black, fixed-depth minimax and alpha-beta, optional capture
   ordering, deterministic tie-breaking, and explicit terminal/no-move results.
3. Search reports nodes, leaves, cutoffs, and elapsed time. An optional node limit
   raises an explicit error and restores all board state; partial results are not returned.
4. Keep `AB.studentAgent`, `AB_solution.studentAgent`, and both modules'
   `get_legal_moves` functions as adapters. White's legacy agent uses depth five
   and returns `((0, 0), (0, 0))` when no move exists. Internal template classes
   and the recursive `ab` helper are replaced by the package API.
5. Assert original sample moves and tactics, every piece rule, terminal states,
   malformed inputs, state restoration, and minimax/alpha-beta equivalence.
6. Provide a JSON CLI and benchmark command with a plain minimax baseline,
   score agreement checks, deterministic node counts, and environment metadata.
7. Document setup, architecture, rules, limitations, provenance, and supported
   resume/portfolio language. Remove the supplied PDF and extracted scratch text
   after validation. Keep public fixture positions as regression data.

## Rules and decisions

- An 8 by 8 board uses zero-based `(row, column)` coordinates.
- King capture ends play. Check, checkmate, castling, promotion, repetition,
  en passant, and standard chess king-safety filtering are outside this variant.
- A king-only position is an immediate draw, even when the kings are adjacent.
- The Squire jumps Manhattan distance two; the Combatant moves orthogonally to
  empty squares and captures diagonally.
- A nonterminal side with no moves receives the static material score at that
  leaf. This search convention is explicit; it does not introduce a passing rule.
- Score is always from white's perspective. Earlier wins and later losses are
  preferred. Equal scores keep the first move in deterministic traversal order.
- Reject invalid piece names, colors, squares, duplicate occupancy or kings, and
  boards with neither king. One missing king represents a completed game.
- Preserve the existing domain. Finance-specific applications, market data,
  GUIs, transposition tables, iterative deepening, and publication are out of scope.

## Acceptance and status

Implementation is complete when formatting/lint checks, the standard-library test suite, installed CLI,
isolated package installation, and benchmark equivalence checks pass locally;
documentation matches those results and the PDF is absent. CI configuration
targets Python 3.12 through 3.14; remote CI execution is separate evidence.

Status: implemented and locally verified on Python 3.12 and 3.14. See
[validation evidence](BENCHMARKS.md) for commands and boundaries. No remote CI
run, publication, repository rename, commit, or push is included in this work.

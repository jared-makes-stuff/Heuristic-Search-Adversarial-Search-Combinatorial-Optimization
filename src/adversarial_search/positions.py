"""Fixed workloads derived from the original public fairy-chess examples."""

DEMO = [
    ("King", "white", (7, 0)),
    ("King", "black", (4, 6)),
    ("Knight", "white", (3, 4)),
]

ENDGAME = [
    ("King", "white", (2, 3)),
    ("King", "black", (0, 4)),
    ("Combatant", "white", (1, 4)),
    ("Combatant", "white", (2, 5)),
    ("Combatant", "black", (7, 0)),
]

TACTICAL = [
    ("King", "white", (2, 3)),
    ("King", "black", (0, 4)),
    ("Squire", "white", (2, 2)),
    ("Rook", "black", (4, 4)),
]

MIDGAME = [
    ("Rook", "white", (6, 3)),
    ("Rook", "black", (0, 1)),
    ("Knight", "white", (2, 4)),
    ("Knight", "black", (3, 1)),
    ("Knight", "white", (5, 6)),
    ("Knight", "black", (5, 7)),
    ("Combatant", "white", (7, 5)),
    ("Combatant", "black", (3, 5)),
    ("Combatant", "white", (2, 2)),
    ("Combatant", "black", (6, 6)),
    ("Bishop", "white", (4, 2)),
    ("Bishop", "white", (5, 4)),
    ("Bishop", "black", (0, 3)),
    ("Bishop", "black", (1, 7)),
    ("Squire", "white", (1, 6)),
    ("Squire", "white", (1, 3)),
    ("Squire", "black", (7, 7)),
    ("Squire", "black", (0, 7)),
    ("King", "black", (0, 0)),
    ("King", "white", (7, 4)),
]

WORKLOADS = {"endgame": ENDGAME, "tactical": TACTICAL, "midgame": MIDGAME}

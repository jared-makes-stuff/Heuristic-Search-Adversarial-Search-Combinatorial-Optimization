##Public testcase 1
b1 = [
    ("Rook", "white", (5, 1)),
    ("Rook", "black", (1, 0)),
    ("Knight", "white", (4, 6)),
    ("Knight", "black", (5, 4)),
    ("Knight", "white", (0, 5)),
    ("Knight", "black", (2, 0)),
    ("Combatant", "white", (4, 0)),
    ("Combatant", "black", (5, 0)),
    ("Combatant", "white", (5, 3)),
    ("Combatant", "black", (5, 6)),
    ("Combatant", "white", (7, 1)),
    ("Combatant", "black", (0, 1)),
    ("Combatant", "white", (0, 4)),
    ("Combatant", "black", (7, 5)),
    ("Bishop", "white", (3, 4)),
    ("Bishop", "white", (1, 1)),
    ("Bishop", "black", (6, 1)),
    ("Bishop", "black", (4, 2)),
    ("King", "black", (0, 6)),
    ("King", "white", (7, 7)),
]

b2 = [
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

b3 = [
    ("Rook", "white", (6, 7)),
    ("Rook", "black", (7, 6)),
    ("Combatant", "white", (5, 6)),
    ("Combatant", "black", (3, 5)),
    ("Combatant", "white", (7, 2)),
    ("Combatant", "black", (2, 2)),
    ("Combatant", "white", (1, 7)),
    ("Combatant", "black", (7, 7)),
    ("Combatant", "white", (2, 1)),
    ("Combatant", "black", (4, 5)),
    ("Bishop", "white", (0, 3)),
    ("Bishop", "white", (3, 3)),
    ("Bishop", "black", (0, 6)),
    ("Bishop", "black", (6, 1)),
    ("Squire", "white", (3, 6)),
    ("Squire", "black", (4, 3)),
    ("King", "black", (0, 0)),
    ("King", "white", (7, 1)),
]

b4 = [
    ("Knight", "white", (3, 4)),
    ("Knight", "black", (7, 7)),
    ("Knight", "white", (0, 7)),
    ("Knight", "black", (7, 4)),
    ("Combatant", "white", (2, 2)),
    ("Combatant", "black", (1, 2)),
    ("Combatant", "white", (2, 7)),
    ("Combatant", "black", (7, 1)),
    ("Combatant", "white", (1, 4)),
    ("Combatant", "black", (6, 4)),
    ("Combatant", "white", (1, 1)),
    ("Combatant", "black", (5, 1)),
    ("Bishop", "white", (4, 1)),
    ("Bishop", "black", (0, 1)),
    ("Squire", "white", (6, 1)),
    ("Squire", "black", (1, 5)),
    ("King", "black", (0, 0)),
    ("King", "white", (7, 6)),
]

## Public testcase 2
## Best move: ((1, 7), (1, 5))
public_m1_1 = [
    ("Combatant", "white", (0, 5)),
    ("Rook", "white", (1, 1)),
    ("Combatant", "white", (1, 4)),
    ("King", "black", (1, 5)),
    ("Combatant", "white", (1, 6)),
    ("Squire", "white", (1, 7)),
    ("Combatant", "white", (2, 5)),
    ("Rook", "black", (4, 3)),
    ("King", "white", (5, 2)),
    ("Rook", "white", (6, 5)),
    ("Bishop", "black", (7, 0)),
    ("Bishop", "black", (7, 3)),
]

## Public testcase 3
## Best move: ((5, 1), (5, 0))
public_m3_1 = [
    ("King", "white", (7, 7)),
    ("King", "black", (0, 0)),
    ("Rook", "white", (6, 1)),
    ("Rook", "white", (5, 1)),
    ("Rook", "black", (6, 5)),
    ("Rook", "black", (6, 6)),
]

## Public testcase 4
## Best move: ((2, 3), (2, 4))
public_m5_1 = [
    ("King", "white", (2, 3)),
    ("King", "black", (0, 4)),
    ("Combatant", "white", (1, 4)),
    ("Combatant", "white", (2, 5)),
    ("Combatant", "black", (7, 0)),
]

## Public testcase 5
## Best move: ((2, 2), (2, 4))
public_e3_1 = [
    ("King", "black", (0, 4)),
    ("Rook", "black", (4, 4)),
    ("King", "white", (2, 3)),
    ("Squire", "white", (2, 2)),
]

## Public testcase 6
## Best move: ((1, 2), (2, 1))
public_e3_2 = [
    ("Rook", "white", (0, 2)),
    ("King", "white", (1, 2)),
    ("Rook", "black", (3, 0)),
    ("King", "black", (6, 2)),
    ("Rook", "black", (6, 4)),
]

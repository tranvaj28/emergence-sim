# Contract: B/S Notation for Cellular Automata Rules

## Overview
The simulator uses the standard "B/S" (Born/Survive) notation to describe cellular automaton rules. This contract defines the syntax and semantics of rule strings.

## Syntax
```
RuleString ::= 'B' <birthDigits> '/' 'S' <surviveDigits>
birthDigits ::= [0-8]+
surviveDigits ::= [0-8]+
```

## Semantics
- `B` (Born) digits indicate the neighbour counts that cause a dead cell to become alive.
- `S` (Survive) digits indicate the neighbour counts that allow a live cell to stay alive.
- Neighbour counts range from 0 to 8 (Moore neighbourhood, including diagonals).
- Digits are concatenated without separators (e.g., `B3/S23`).
- Order of digits does not matter; duplicates are ignored.

## Examples
- Conway's Game of Life: `B3/S23`
- HighLife: `B36/S23`
- Day & Night: `B3678/S34678`

## Preset Rules
The simulator ships with three preset rules, accessible via keyboard shortcuts:

| Preset Name       | Rule String     | Shortcut |
|-------------------|-----------------|----------|
| Conway's Game of Life | `B3/S23`   | 1        |
| HighLife          | `B36/S23`      | 2        |
| Day & Night       | `B3678/S34678` | 3        |

## Implementation Notes
- Rule strings are case‑insensitive (`b3/s23` is acceptable).
- Extra whitespace is ignored.
- The parser must validate that digits are between 0 and 8.
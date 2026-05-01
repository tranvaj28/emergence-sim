# Data Model: Cellular Automata Simulator

## Entities

### Grid
- **Type**: `numpy.ndarray` with dtype `bool`
- **Shape**: `(rows, cols)` where rows = cols = 100 (configurable)
- **Purpose**: Represents the current state of the cellular automaton grid (True = alive, False = dead)
- **Constraints**: Toroidal wrapping at edges.

### RuleSet
- **Type**: `dataclass` or `namedtuple`
- **Fields**:
  - `name: str` (e.g., "Conway's Game of Life")
  - `born: set[int]` (birth conditions, e.g., {3})
  - `survive: set[int]` (survival conditions, e.g., {2,3})
- **Purpose**: Encodes a cellular automaton rule in B/S notation.
- **Presets**: Conway (B3/S23), HighLife (B36/S23), Day & Night (B3678/S34678).

### SimulationState
- **Type**: `dataclass`
- **Fields**:
  - `grid: Grid`
  - `generation: int` (current generation number, starting at 0)
  - `rule: RuleSet`
  - `playing: bool` (whether simulation is advancing automatically)
  - `speed: int` (steps per second, range 1‑60)
- **Purpose**: Holds the complete runtime state of the simulation.

### HistoryBuffer
- **Type**: `collections.deque` with `maxlen=500`
- **Element type**: `Grid` (numpy bool array)
- **Purpose**: Stores previous grid states to support rewind (step‑backward).
- **Operations**:
  - `push(grid)` → adds current grid to buffer (when stepping forward)
  - `pop()` → retrieves most recent historical grid (when stepping backward)
- **Constraints**: FIFO, oldest generation discarded when buffer full.

### Statistics
- **Type**: `dataclass`
- **Fields**:
  - `live_count: int` (number of alive cells in current grid)
  - `live_percentage: float` (live_count / total_cells)
  - `population_history: list[int]` (circular buffer of last 200 live counts)
- **Purpose**: Tracks population metrics for display in HUD.

## Relationships
- One `SimulationState` contains one `Grid`, one `RuleSet`, one `HistoryBuffer`, and one `Statistics`.
- `HistoryBuffer` stores snapshots of `Grid` over time.
- `Statistics` updates each generation based on `Grid`.

## Validation Rules
- Grid dimensions must be positive integers.
- RuleSet born and survive sets must contain integers 0–8 inclusive.
- Speed must be between 1 and 60 steps per second.
- Generation number must be non‑negative.
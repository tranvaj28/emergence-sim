# Quick Start: Cellular Automata Simulator

## Prerequisites
- Python 3.11 or later
- pip (Python package manager)

## Setup
1. Clone the repository.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   (If no requirements.txt exists, install manually: `pip install pygame numpy`)

## Running the Simulator
```bash
python src/main.py
```

## Running Tests
```bash
pytest tests/
```

## Project Structure
- `src/main.py` – Entry point, PyGame event loop
- `src/grid.py` – Grid state and rule application
- `src/hud.py` – Heads‑up display (population stats, graph)
- `src/rules.py` – Rule set definitions and parser
- `src/config.py` – Configuration constants (grid size, colors, etc.)
- `tests/` – Unit and integration tests

## Key Controls
- **Space**: Play/pause simulation
- **→** (right arrow): Step forward one generation (when paused)
- **←** (left arrow): Step backward one generation (when paused, if history available)
- **R**: Reset grid to all‑dead, clear history
- **S**: Seed random pattern (30% density)
- **+/-**: Increase/decrease simulation speed (1–60 steps/sec)
- **1,2,3**: Switch rule presets (Conway, HighLife, Day & Night)

## Development Notes
- The grid is a 100×100 toroidal array of Boolean values.
- History buffer stores up to 500 previous generations for rewind.
- Population graph shows the last 200 generations.
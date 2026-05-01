# Emergence Simulator

A desktop cellular automata simulator built with Python and PyGame for exploring emergent behavior through Conway's Game of Life and alternative rule sets.

## Features

- **100×100 toroidal grid** rendered at 60 FPS
- **Draw mode** for painting initial states (left‑click alive, right‑click dead)
- **Conway's Game of Life** (B3/S23) with automatic simulation
- **Playback controls**: play/pause, step forward/backward, speed adjustment (1–60 steps/sec)
- **500‑generation history buffer** for rewind
- **Alternative rule presets**: HighLife (B36/S23), Day & Night (B3678/S34678)
- **Live population statistics** and 200‑generation graph

## Quick Start

### Prerequisites
- Python 3.11 or later
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd emergence-sim
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Simulator
```bash
python src/main.py
```

## Controls

| Key | Action |
|-----|--------|
| **Space** | Play/pause simulation |
| **→** (right arrow) | Step forward one generation (when paused) |
| **←** (left arrow) | Step backward one generation (when paused, if history available) |
| **R** | Reset grid to all‑dead, clear history |
| **S** | Seed random pattern (30% density) |
| **+** / **‑** | Increase/decrease simulation speed (1–60 steps/sec) |
| **1** | Conway's Game of Life (B3/S23) |
| **2** | HighLife (B36/S23) |
| **3** | Day & Night (B3678/S34678) |

## Project Structure

```
src/
├── main.py          # Pygame event loop, input handling
├── grid.py          # Grid state, rule application, neighbor sum, history deque
├── hud.py           # Stats overlay, population graph
├── rules.py         # Rule set definitions and B/S parser
└── config.py        # Constants (grid size, colors, default speed, MAX_HISTORY)

tests/
├── unit/
│   ├── test_grid.py
│   ├── test_rules.py
│   └── test_hud.py
└── integration/
    └── test_simulation.py
```

## Development

Run tests:
```bash
pytest tests/
```

## License

[MIT](LICENSE) – see LICENSE file for details.
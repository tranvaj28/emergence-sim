# Emergence simulator — project spec
v0.1 · ready for /speckit.specify

## Overview
A desktop application that lets the user explore cellular automata rules and observe emergent behavior in real time. The simulator runs on a 2D grid and supports Conway's Game of Life out of the box, with the ability to define and load custom rule sets. The user can draw initial states, control simulation speed, step frame-by-frame, and observe population statistics live.

**Stack:** Python 3.11+, Pygame 2.x, NumPy — single window, no network, runs fully offline.

## Goals
- Make emergent complexity visually immediate — changes in rules should produce dramatic visible effects within seconds
- Keep the rule system simple enough to explain in one sentence, extensible enough to support non-Conway rule sets
- Serve as a clean first SDD sandbox: bounded scope, clear data model, testable acceptance criteria

## Out of scope
- No 3D grid
- No network / multiplayer
- No non-binary cell states (for now)
- No file save/load (v1)

## User stories

### US-01 · Grid rendering
As a user, I want to see a grid of cells rendered in a Pygame window so that I can observe the simulation visually.

Acceptance criteria:
- Grid is at least 100×100 cells, configurable at launch via a constant
- Live cells render in a distinct color from dead cells
- Grid lines are visible but subtle (low-contrast, toggleable)
- Window is resizable; grid scales to fit without distorting cell aspect ratio

### US-02 · Conway's Game of Life rules
As a user, I want the default rule set to be Conway's Game of Life so that I have a well-known baseline to explore.

Acceptance criteria:
- A live cell with 2 or 3 live neighbours survives
- A dead cell with exactly 3 live neighbours becomes alive
- All other cells die or stay dead
- Neighbourhood is Moore (8 surrounding cells)
- Grid wraps at edges (toroidal topology)

### US-03 · Draw mode
As a user, I want to click and drag on the grid to toggle cells alive or dead so that I can set up interesting initial conditions.

Acceptance criteria:
- Left-click sets cells to alive; right-click sets cells to dead
- Click-and-drag works smoothly at 60fps without skipping cells
- Drawing is only active when simulation is paused


### US-04 · Simulation controls
As a user, I want playback controls so that I can start, pause, step forward, step back, and reset the simulation.

Acceptance criteria:
- Space toggles play/pause
- → advances one generation when paused
- ← rewinds one generation when paused, if history is available
- R resets the grid to all-dead and clears history
- S seeds the grid with a random pattern at configurable density (default 30%) and clears history
- Current generation count is displayed in the window title or HUD
- If no history is available, ← is silently ignored (no error)

### US-05 · Speed control
As a user, I want to control simulation speed so that I can observe slow emergence or fast convergence.

Acceptance criteria:
- + / - keys adjust steps per second (range: 1–60)
- Current speed is shown in the HUD
- Speed change takes effect on the next tick, not the current one

### US-06 · Live population stats
As a user, I want to see a live population count and a small history graph so that I can observe population dynamics over time.

Acceptance criteria:
- HUD shows current live cell count and percentage of grid
- A simple line graph in the HUD shows population over the last 200 generations
- Graph updates every generation, even at high speed

### US-07 · Custom rule sets
As a user, I want to switch between named rule sets so that I can explore behaviors beyond Conway.

Acceptance criteria:
- Rules are expressed in B/S notation (e.g. B3/S23 for Conway)
- At least 3 named presets ship: Conway (B3/S23), HighLife (B36/S23), Day & Night (B3678/S34678)
- 1 / 2 / 3 keys switch presets; current rule is shown in HUD
- Switching rule resets generation count but preserves the current grid state

## Technical design notes

### Data model
- Grid state is a NumPy bool array of shape (rows, cols) — fast for neighbour-sum convolutions
- Next generation computed via scipy.signal.convolve2d or manual roll-based sum — no Python loops over cells
- Rule set is a dataclass: name: str, born: set[int], survive: set[int]
- History is stored as a collections.deque(maxlen=500) of NumPy bool arrays for rewind support
- At 100×100 each frame is ~10KB, so 500 frames ≈ 5MB; at 200×200 ≈ 40MB — document tradeoff in config.py

### Architecture
- main.py — Pygame event loop, input handling
- grid.py — Grid state, rule application, neighbour sum, history deque
- hud.py — Stats overlay, population graph
- rules.py — Rule set definitions and B/S parser
- config.py — All magic numbers (grid size, colours, default speed, MAX_HISTORY)

### Performance target
- 100×100 grid must simulate and render at 60fps on a mid-range laptop
- 200×200 must sustain at least 30fps

### History buffer (addition to grid.py):
- Grid state is pushed to a deque (maxlen configurable, default 500) on every forward step
- Rewinding pops from the deque and restores grid state — no backwards computation
- History is cleared on R, S, and rule-set switch
- HUD shows rewind depth when rewound, e.g. "gen 142 [-58]"
- Must use collections.deque(maxlen=MAX_HISTORY), not a plain list
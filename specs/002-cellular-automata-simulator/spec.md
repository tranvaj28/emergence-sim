# Feature Specification: Desktop Cellular Automata Simulator

**Feature Branch**: `002-cellular-automata-simulator`  
**Created**: Mon Mar 23 2026  
**Status**: Draft  
**Input**: User description: "A desktop cellular automata simulator built with Python and Pygame. The user can explore emergent behavior through Conway's Game of Life and alternative rule sets (HighLife, Day & Night) expressed in B/S notation. Features include: a 100x100 toroidal grid rendered at 60fps, draw mode for painting initial states, play/pause/step-forward/step-back controls with a 500-generation history buffer for rewind, variable simulation speed (1-60 steps/sec), live population stats with a 200-generation graph, and keyboard shortcuts to switch between rule presets. Full spec is in SPEC.md."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Draw and observe Conway's Game of Life (Priority: P1)

As a user, I can draw initial patterns on a 100x100 toroidal grid and observe Conway's Game of Life simulation advancing automatically at a fixed speed, so that I can explore emergent behavior without needing advanced controls.

**Why this priority**: This is the core value proposition—enabling observation of emergent behavior from simple rules. Without drawing and automatic simulation, no other features are meaningful.

**Independent Test**: Can be fully tested by launching the simulator, drawing a pattern, and verifying that cells evolve according to Conway's rules without any user interaction beyond initial drawing.

**Acceptance Scenarios**:

1. **Given** an empty grid, **When** the user draws a glider pattern, **Then** the pattern moves across the grid toroidally every 4 generations.
2. **Given** a randomly filled grid, **When** simulation runs, **Then** the grid updates at 60 frames per second and cells follow Conway's B3/S23 rules.

---

### User Story 2 - Control simulation playback (Priority: P2)

As a user, I can control simulation playback (play/pause/step forward/step back) and adjust simulation speed, so that I can analyze evolution at my own pace and rewind to interesting moments.

**Why this priority**: Interactive control is essential for detailed observation, debugging, and exploration of specific generations.

**Independent Test**: Can be tested by pausing simulation, stepping forward/backward through the history buffer, and verifying that the grid state matches the expected generation.

**Acceptance Scenarios**:

1. **Given** a running simulation, **When** the user presses pause, **Then** the grid stops updating and the current generation is preserved.
2. **Given** a simulation with at least 10 generations of history, **When** the user steps backward 5 times, **Then** the grid displays the state from 5 generations earlier.
3. **Given** a paused simulation, **When** the user adjusts speed slider to 30 steps/sec, **Then** after pressing play, the simulation advances at approximately 30 steps per second.

---

### User Story 3 - Switch between rule presets (Priority: P3)

As a user, I can switch between different cellular automata rule presets (HighLife, Day & Night) using keyboard shortcuts, so that I can compare emergent behaviors across rule sets.

**Why this priority**: Alternative rule sets expand the exploratory possibilities and are a key differentiator for the simulator.

**Independent Test**: Can be tested by loading a known pattern, switching rule presets, and verifying that the pattern evolves according to the new rule set.

**Acceptance Scenarios**:

1. **Given** a grid with a replicator pattern known to work under HighLife (B36/S23), **When** the user switches to HighLife preset, **Then** the pattern replicates as expected.
2. **Given** a grid running Conway's Game of Life, **When** the user presses the shortcut for Day & Night (B3678/S34678), **Then** the simulation immediately adopts the new rules and cells evolve accordingly.

---

### User Story 4 - View population statistics and graph (Priority: P4)

As a user, I can view live population statistics and a 200-generation graph, so that I can track population trends over time and identify stable patterns.

**Why this priority**: Quantitative feedback enhances understanding of simulation dynamics and helps identify interesting behaviors.

**Independent Test**: Can be tested by running a simulation and verifying that the population count updates each generation and the graph displays the last 200 generations.

**Acceptance Scenarios**:

1. **Given** a simulation with a known oscillating pattern (period 2), **When** the simulation runs for 10 generations, **Then** the population graph shows a regular oscillation with period 2.
2. **Given** a simulation with a glider, **When** the glider moves off one edge and reappears on the opposite side (toroidal wrap), **Then** the population count remains constant.

---

### Edge Cases

- What happens when the history buffer reaches 500 generations? New generations should displace oldest generations (FIFO).
- How does system handle extreme simulation speed (1 step/sec vs 60 steps/sec)? The UI should remain responsive and rendering smooth.
- What occurs when the user draws while simulation is running? Drawing should affect the current generation immediately.
- How does the graph handle when fewer than 200 generations have elapsed? It should display available data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render a 100x100 toroidal grid at 60 frames per second.
- **FR-002**: System MUST implement Conway's Game of Life rules (B3/S23).
- **FR-003**: Users MUST be able to draw (paint) live and dead cells on the grid with mouse interaction.
- **FR-004**: System MUST provide play, pause, step‑forward, and step‑backward controls.
- **FR-005**: System MUST maintain a 500‑generation history buffer to support stepping backward.
- **FR-006**: System MUST allow variable simulation speed between 1 and 60 steps per second.
- **FR-007**: System MUST display live population count (percentage of live cells) and a graph of the last 200 generations.
- **FR-008**: System MUST include keyboard shortcuts to switch between at least three rule presets: Conway's Game of Life, HighLife (B36/S23), and Day & Night (B3678/S34678).
- **FR-009**: System MUST support only the three preset rule sets (Conway's Game of Life, HighLife, Day & Night); custom rule definition is out of scope for this version.

### Key Entities *(include if feature involves data)*

- **Grid**: A 100×100 toroidal array of cells; each cell is either alive or dead.
- **RuleSet**: A cellular automaton rule expressed in B/S notation (birth/survival conditions).
- **SimulationState**: Current grid, current generation number, current rule set, playback status (playing/paused), speed setting.
- **HistoryBuffer**: FIFO buffer of up to 500 previous grid states, enabling rewind.
- **Statistics**: Live population count and a time‑series of population values for the last 200 generations.

## Assumptions

- The simulator runs on desktop operating systems (Windows, macOS, Linux) with standard hardware capable of 60 FPS rendering.
- Users are familiar with basic cellular automata concepts (live/dead cells, generations).
- The grid size is fixed at 100x100; resizing is out of scope.
- Toroidal wrapping is applied to all edges.
- Custom rule definition and pattern save/load functionality are out of scope for this version.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can draw a pattern and see it evolve according to the selected rule set within 1 second of starting the simulation.
- **SC-002**: Simulation maintains a consistent 60 FPS rendering while stepping at up to 60 steps per second on standard hardware.
- **SC-003**: Users can step backward through the full 500‑generation history buffer without any visible delay (<200 ms per step).
- **SC-004**: Switching between rule presets via keyboard shortcuts takes less than 1 second and does not disrupt the simulation state.
- **SC-005**: Population graph updates in real‑time (within 100 ms of each generation step) and accurately reflects the last 200 generations.
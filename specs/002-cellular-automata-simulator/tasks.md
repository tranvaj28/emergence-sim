---
description: "Task list for Desktop Cellular Automata Simulator implementation"
---

# Tasks: Desktop Cellular Automata Simulator

**Input**: Design documents from `/specs/002-cellular-automata-simulator/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are included based on acceptance scenarios and independent test criteria in spec.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (as per plan.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/, tests/unit/, tests/integration/
- [x] T002 Create requirements.txt with pygame>=2.5.0 and numpy>=1.24
- [x] T003 [P] Create .gitignore for Python/Pygame projects
- [x] T004 [P] Create README.md with project overview

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create config.py with constants (GRID_SIZE, CELL_SIZE, COLORS, SPEED_RANGE, MAX_HISTORY, GRAPH_HISTORY) in src/config.py
- [x] T006 [P] Create RuleSet dataclass with fields (name, born, survive) and B/S parser in src/rules.py
- [x] T007 [P] Create Grid class with numpy boolean array, toroidal neighbor count helper using numpy.roll for wrap-around, and history buffer attribute (collections.deque) in src/grid.py. 
- Implement history buffer in `grid.py` using `collections.deque(maxlen=MAX_HISTORY)`
  - `MAX_HISTORY` is read from `config.py` (default: 500)
  - Every call to `step_forward()` pushes the current grid state onto the deque before computing the next generation
  - `step_back()` pops from the deque and restores grid state; if deque is empty, does nothing
  - History is cleared on reset, reseed, and rule-set switch
  - Grid state stored as a copy (`array.copy()`), not a reference — otherwise all history entries point to the same mutating array
- [x] T008 Create main.py skeleton with Pygame window initialization and event loop (no simulation yet) in src/main.py
- [x] T009 [P] Create hud.py skeleton (empty module) in src/hud.py
- [x] T010 [P] Create basic test structure: __init__.py files in tests/unit/ and tests/integration/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Draw and observe Conway's Game of Life (Priority: P1) 🎯 MVP

**Goal**: User can draw patterns on a 100×100 toroidal grid and observe Conway's Game of Life simulation advancing automatically.

**Independent Test**: Launch simulator, draw a glider pattern, verify it moves across grid toroidally every 4 generations.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T011 [P] [US1] Test Conway rule set parsing in tests/unit/test_rules.py
- [x] T012 [P] [US1] Test Grid neighbor count with toroidal wrap including edge cells and wrap-around behavior in tests/unit/test_grid.py
- [x] T013 [P] [US1] Test Conway rule application on known patterns in tests/unit/test_grid.py
- [x] T014 [P] [US1] Integration test: draw glider and verify movement in tests/integration/test_simulation.py

### Implementation for User Story 1

- [x] T015 [P] [US1] Implement Conway rule preset (B3/S23) in src/rules.py
- [x] T016 [US1] Implement Grid.apply_rule(rule) method for Conway's Game of Life in src/grid.py
- [x] T017 [US1] Implement mouse drawing (left‑click alive, right‑click dead) in src/main.py
- [x] T018 [US1] Implement automatic simulation stepping at fixed speed in src/main.py
- [x] T019 [US1] Connect Grid to main loop: update grid each frame when playing in src/main.py
- [x] T020 [US1] Add basic HUD showing generation count and play/pause status in src/hud.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Control simulation playback (Priority: P2)

**Goal**: User can control playback (play/pause/step forward/step back) and adjust simulation speed.

**Independent Test**: Pause simulation, step forward/backward through history buffer, verify grid state matches expected generation.

### Tests for User Story 2

- [x] T021 [P] [US2] Test HistoryBuffer FIFO behavior (maxlen=500) including empty buffer, full buffer, push/pop operations in tests/unit/test_grid.py
- [x] T022 [P] [US2] Test step‑forward and step‑backward with history in tests/unit/test_grid.py
- [x] T023 [P] [US2] Integration test: pause, step, adjust speed in tests/integration/test_simulation.py

### Implementation for User Story 2

- [x] T024 [P] [US2] Implement HistoryBuffer class (wrapper around collections.deque with maxlen=config.MAX_HISTORY) in src/grid.py
- [x] T025 [US2] Integrate HistoryBuffer with Grid: push copy of current grid on step forward, pop most recent grid on step back and restore it in src/grid.py
- [x] T026 [US2] Implement play/pause toggle (Space key) in src/main.py
- [x] T027 [US2] Implement step‑forward (→) and step‑backward (←) controls in src/main.py
- [x] T028 [US2] Implement speed adjustment (+/- keys) with range 1–60 steps/sec in src/main.py
- [x] T029 [US2] Update HUD to show current speed and play/pause state in src/hud.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Switch between rule presets (Priority: P3)

**Goal**: User can switch between different cellular automata rule presets (HighLife, Day & Night) using keyboard shortcuts.

**Independent Test**: Load known pattern, switch rule presets, verify pattern evolves according to new rule set.

### Tests for User Story 3

- [x] T030 [P] [US3] Test HighLife and Day & Night rule parsing in tests/unit/test_rules.py
- [x] T031 [P] [US3] Test rule switching preserves grid state in tests/unit/test_grid.py
- [x] T032 [P] [US3] Integration test: switch rules and verify pattern evolution in tests/integration/test_simulation.py

### Implementation for User Story 3

- [x] T033 [P] [US3] Implement HighLife (B36/S23) and Day & Night (B3678/S34678) presets in src/rules.py
- [x] T034 [US3] Implement rule switching via keyboard shortcuts (1,2,3) in src/main.py
- [x] T035 [US3] Update Grid.apply_rule to use current RuleSet from SimulationState in src/grid.py
- [x] T036 [US3] Clear history buffer when rule changes (as per spec) in src/grid.py
- [x] T037 [US3] Update HUD to show current rule name in src/hud.py

**Checkpoint**: All three rule presets should be switchable without disrupting simulation

---

## Phase 6: User Story 4 - View population statistics and graph (Priority: P4)

**Goal**: User can view live population statistics and a 200‑generation graph.

**Independent Test**: Run simulation with oscillating pattern, verify population graph shows regular oscillation.

### Tests for User Story 4

- [x] T038 [P] [US4] Test Statistics tracking (live count, percentage) in tests/unit/test_hud.py
- [x] T039 [P] [US4] Test population history circular buffer (last 200 generations) in tests/unit/test_hud.py
- [x] T040 [P] [US4] Integration test: verify graph updates each generation in tests/integration/test_simulation.py

### Implementation for User Story 4

- [x] T041 [P] [US4] Implement Statistics class with live_count and population_history in src/hud.py
- [x] T042 [US4] Integrate Statistics with simulation loop: update each generation in src/main.py
- [ ] T043 [US4] Implement population graph rendering using pygame.draw.lines in src/hud.py
- [ ] T044 [US4] Add graph to HUD display (position, scaling) in src/hud.py
- [ ] T045 [US4] Update HUD to show live count and percentage in src/hud.py

**Checkpoint**: Population statistics and graph should update in real‑time

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T046 [P] Performance optimization: limit redraws to changed cells in src/main.py
- [ ] T047 [P] Add keyboard shortcuts help to HUD in src/hud.py
- [ ] T048 [P] Implement grid reset (R key) and random seed (S key) with history buffer clearance in src/main.py
- [ ] T049 [P] Code cleanup and refactoring across all modules
- [ ] T050 [P] Additional unit tests for edge cases (history buffer full, extreme speeds) in tests/unit/
- [ ] T051 Run quickstart.md validation: ensure setup and running instructions work
- [ ] T052 Update documentation with final feature details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Depends on Grid and HistoryBuffer (part of US1/Foundation)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on RuleSet (Foundation) and Grid
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Depends on simulation loop (US1) and HUD

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Core data structures before services
- Services before UI integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Test Conway rule set parsing in tests/unit/test_rules.py"
Task: "Test Grid neighbor count with toroidal wrap in tests/unit/test_grid.py"
Task: "Test Conway rule application on known patterns in tests/unit/test_grid.py"

# Launch implementation tasks that can run in parallel:
Task: "Implement Conway rule preset (B3/S23) in src/rules.py"
Task: "Implement mouse drawing (left‑click alive, right‑click dead) in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2  
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

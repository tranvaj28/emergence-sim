"""Unit tests for Grid class and neighbor counting."""

import numpy as np
import pytest
from src.rules import CONWAY, DAY_NIGHT, HIGHLIFE, RuleSet

from src.grid import Grid, HistoryBuffer


def test_grid_initialization():
    """Grid should start with all cells dead."""
    grid = Grid(rows=5, cols=5)
    assert grid.rows == 5
    assert grid.cols == 5
    assert np.all(grid.cells == False)  # noqa: E712
    assert len(grid.history) == 0


def test_get_set_cell():
    """Setting and getting individual cells."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(2, 3, True)
    assert grid.get_cell(2, 3) is True
    assert grid.get_cell(2, 2) is False

    grid.set_cell(0, 0, True)
    assert grid.get_cell(0, 0) is True


def test_toggle_cell():
    """Toggling cell state."""
    grid = Grid(rows=5, cols=5)
    grid.toggle_cell(1, 1)
    assert grid.get_cell(1, 1) is True
    grid.toggle_cell(1, 1)
    assert grid.get_cell(1, 1) is False


def test_clear():
    """Clearing the grid resets all cells to dead."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(0, 0, True)
    grid.set_cell(1, 1, True)
    grid.clear()
    assert np.all(grid.cells == False)  # noqa: E712
    assert len(grid.history) == 0


def test_neighbor_counts_all_dead():
    """Neighbor counts for an empty grid are all zero."""
    grid = Grid(rows=3, cols=3)
    counts = grid.neighbor_counts()
    expected = np.zeros((3, 3), dtype=int)
    assert np.array_equal(counts, expected)


def test_neighbor_counts_single_cell_center():
    """A single live cell in the center has eight neighbors (all dead)."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(2, 2, True)
    counts = grid.neighbor_counts()

    # All cells should have neighbor count 1 except the center which has 0
    # (because neighbor counts exclude the cell itself)
    assert counts[2, 2] == 0
    # The eight surrounding cells should have count 1
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dy == 0 and dx == 0:
                continue
            assert counts[2 + dy, 2 + dx] == 1
    # Cells farther away should have count 0
    assert counts[0, 0] == 0
    assert counts[4, 4] == 0


def test_neighbor_counts_single_cell_edge_wrap():
    """A live cell on the left edge should wrap to the right edge."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(2, 0, True)  # left edge, middle row
    counts = grid.neighbor_counts()

    # The cell itself has 0 neighbors
    assert counts[2, 0] == 0
    # Immediate neighbors (including wrap‑around)
    # Left side wraps to column 4 (right edge)
    assert counts[1, 4] == 1  # top‑left wrapped
    assert counts[2, 4] == 1  # left wrapped
    assert counts[3, 4] == 1  # bottom‑left wrapped
    # Normal right side (column 1)
    assert counts[1, 1] == 1  # top‑right
    assert counts[2, 1] == 1  # right
    assert counts[3, 1] == 1  # bottom‑right
    # Above and below (same column 0)
    assert counts[1, 0] == 1  # top
    assert counts[3, 0] == 1  # bottom


def test_neighbor_counts_single_cell_corner_wrap():
    """A live cell in the top‑left corner wraps to bottom‑right."""
    grid = Grid(rows=3, cols=3)
    grid.set_cell(0, 0, True)
    counts = grid.neighbor_counts()

    # Cell itself
    assert counts[0, 0] == 0
    # Neighbors (all other cells) should have count 1
    for r in range(3):
        for c in range(3):
            if r == 0 and c == 0:
                continue
            assert counts[r, c] == 1


def test_neighbor_counts_all_alive():
    """A completely filled grid: each cell has 8 neighbors."""
    grid = Grid(rows=4, cols=4)
    grid.cells.fill(True)
    counts = grid.neighbor_counts()
    # Every cell should have exactly 8 neighbors (all eight surrounding cells are alive)
    assert np.all(counts == 8)


def test_neighbor_counts_pattern():
    """Test a specific pattern to verify neighbor counts."""
    grid = Grid(rows=3, cols=3)
    # Create a small blinker pattern (vertical line)
    grid.set_cell(0, 1, True)
    grid.set_cell(1, 1, True)
    grid.set_cell(2, 1, True)

    counts = grid.neighbor_counts()
    # Middle cell (1,1) has two alive neighbors (above and below) → count 2
    assert counts[1, 1] == 2
    # Top cell (0,1) has two alive neighbors (middle and bottom via wrap) → count 2
    assert counts[0, 1] == 2
    # Left of middle (1,0) has three alive neighbors (top, middle, bottom) → count 3
    assert counts[1, 0] == 3
    # Right of middle (1,2) similarly count 3
    assert counts[1, 2] == 3


def test_copy():
    """Copying a grid creates an independent duplicate."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(2, 2, True)
    grid_copy = grid.copy()
    # They should have the same cell states initially
    assert np.array_equal(grid.cells, grid_copy.cells)
    # Modifying the original should not affect the copy
    grid.set_cell(0, 0, True)
    assert grid_copy.get_cell(0, 0) is False


def test_history_push_pop():
    """Basic history buffer operations."""
    grid = Grid(rows=3, cols=3)
    grid.set_cell(0, 0, True)
    grid.push_to_history()
    original_cells = grid.cells.copy()

    grid.set_cell(1, 1, True)
    assert grid.get_cell(0, 0) is True
    assert grid.get_cell(1, 1) is True

    restored = grid.pop_from_history()
    assert restored is not None
    assert np.array_equal(grid.cells, original_cells)
    assert grid.get_cell(1, 1) is False


def test_history_empty_pop():
    """Popping from an empty history returns None."""
    grid = Grid(rows=3, cols=3)
    assert grid.pop_from_history() is None


@pytest.fixture
def sample_grid():
    return Grid(rows=5, cols=5)


class TestHistoryBuffer:
    """Tests for HistoryBuffer FIFO behavior."""

    def test_init_default_maxlen(self):
        """HistoryBuffer should default to config.MAX_HISTORY."""
        buf = HistoryBuffer()
        assert buf.maxlen == 500

    def test_init_custom_maxlen(self):
        """HistoryBuffer accepts a custom maxlen."""
        buf = HistoryBuffer(maxlen=10)
        assert buf.maxlen == 10

    def test_push_pop(self):
        """Pop returns the most recently pushed grid state."""
        buf = HistoryBuffer()
        g1 = Grid(rows=3, cols=3)
        g1.set_cell(0, 0, True)
        g2 = Grid(rows=3, cols=3)
        g2.set_cell(1, 1, True)

        buf.push(g1)
        buf.push(g2)

        result = buf.pop()
        assert result is not None
        assert result.get_cell(1, 1) is True
        assert result.get_cell(0, 0) is False

        result = buf.pop()
        assert result is not None
        assert result.get_cell(0, 0) is True
        assert result.get_cell(1, 1) is False

    def test_pop_empty_returns_none(self):
        """Popping from an empty buffer returns None."""
        buf = HistoryBuffer()
        assert buf.pop() is None

    def test_pop_after_single_push(self):
        """Push once, pop once — should get the pushed state."""
        buf = HistoryBuffer()
        g = Grid(rows=3, cols=3)
        g.set_cell(2, 2, True)
        buf.push(g)
        result = buf.pop()
        assert result is not None
        assert result.get_cell(2, 2) is True

    def test_maxlen_fifo_discard_oldest(self):
        """When buffer exceeds maxlen, oldest item is discarded (FIFO)."""
        buf = HistoryBuffer(maxlen=3)
        grids = []
        for i in range(4):
            g = Grid(rows=2, cols=2)
            g.set_cell(0, 0, bool(i % 2))
            buf.push(g)
            grids.append(g)

        # Buffer size should be at most 3
        assert len(buf) == 3
        # The oldest (index 0) should have been discarded
        result = buf.pop()
        assert result is not None
        assert np.array_equal(result.cells, grids[1].cells)

    def test_maxlen_keeps_newest_items(self):
        """After exceeding maxlen, buffer retains the N most recent items."""
        buf = HistoryBuffer(maxlen=3)
        for i in range(5):
            g = Grid(rows=2, cols=2)
            g.set_cell(0, 0, bool(i % 2))
            buf.push(g)

        # Pop all items — should get items 4, 3, 2 (most recent first)
        popped = []
        while True:
            item = buf.pop()
            if item is None:
                break
            popped.append(item)
        assert len(popped) == 3

    def test_push_does_not_affect_original(self):
        """Grid passed to push should be copied internally."""
        buf = HistoryBuffer()
        g = Grid(rows=3, cols=3)
        g.set_cell(0, 0, True)
        buf.push(g)
        g.set_cell(0, 0, False)
        result = buf.pop()
        assert result is not None
        assert result.get_cell(0, 0) is True

    def test_len_empty(self):
        """Len of empty buffer is 0."""
        buf = HistoryBuffer()
        assert len(buf) == 0

    def test_len_after_push(self):
        """Len increases after each push."""
        buf = HistoryBuffer(maxlen=10)
        for i in range(5):
            g = Grid(rows=2, cols=2)
            buf.push(g)
        assert len(buf) == 5

    def test_len_after_pop(self):
        """Len decreases after each pop."""
        buf = HistoryBuffer(maxlen=10)
        for i in range(5):
            g = Grid(rows=2, cols=2)
            buf.push(g)
        buf.pop()
        buf.pop()
        assert len(buf) == 3

    def test_clear(self):
        """Clear removes all items from the buffer."""
        buf = HistoryBuffer(maxlen=10)
        for i in range(4):
            g = Grid(rows=2, cols=2)
            buf.push(g)
        buf.clear()
        assert len(buf) == 0
        assert buf.pop() is None


def test_apply_rule_conway_blinker():
    """Test Conway rule application on a blinker pattern."""
    grid = Grid(rows=5, cols=5)
    # Create vertical blinker in middle
    grid.set_cell(2, 1, True)
    grid.set_cell(2, 2, True)
    grid.set_cell(2, 3, True)
    grid.current_rule = RuleSet.from_string("Conway", "B3/S23")
    grid.apply_rule()
    # Should become horizontal blinker
    assert grid.get_cell(1, 2) is True
    assert grid.get_cell(2, 2) is True
    assert grid.get_cell(3, 2) is True
    # Other cells should be dead
    for r in range(5):
        for c in range(5):
            if (r, c) not in [(1, 2), (2, 2), (3, 2)]:
                assert grid.get_cell(r, c) is False


def test_different_rules_different_results():
    """Different rules applied to the same initial state yield different results."""
    grid_conway = Grid(rows=7, cols=7)
    grid_highlife = Grid(rows=7, cols=7)

    # Ring of 6 cells around center — center will have exactly 6 neighbors
    ring = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0)]
    for dr, dc in ring:
        grid_conway.set_cell(3 + dr, 3 + dc, True)
        grid_highlife.set_cell(3 + dr, 3 + dc, True)

    grid_conway.current_rule = CONWAY
    grid_conway.apply_rule()
    grid_highlife.current_rule = HIGHLIFE
    grid_highlife.apply_rule()

    # Center (3,3) has 6 neighbors: Conway B3 doesn't include 6, HighLife B36 does
    assert grid_conway.get_cell(3, 3) is False, "Center should be dead under Conway"
    assert grid_highlife.get_cell(3, 3) is True, "Center should be alive under HighLife"


def test_rule_switch_uses_current_state():
    """Sequential rule applications correctly chain on current grid state."""
    grid = Grid(rows=7, cols=7)
    tub = [(3, 2), (2, 3), (3, 4), (4, 3)]
    for r, c in tub:
        grid.set_cell(r, c, True)

    # Step 1: Apply Conway — tub is stable (each cell has 2 neighbors, S23 includes 2)
    grid.current_rule = CONWAY
    grid.apply_rule()
    for r, c in tub:
        assert grid.get_cell(r, c) is True, "Tub cell should survive under Conway"

    # Step 2: Apply Day & Night — tub dies (2 neighbors, S34678 excludes 2)
    grid.current_rule = DAY_NIGHT
    grid.apply_rule()
    assert np.sum(grid.cells) == 0, "Tub should die under Day & Night"

    # Counterfactual: Conway twice keeps tub alive
    grid_conway2 = Grid(rows=7, cols=7)
    grid_conway2.current_rule = CONWAY
    for r, c in tub:
        grid_conway2.set_cell(r, c, True)
    grid_conway2.apply_rule()
    grid_conway2.apply_rule()
    assert np.sum(grid_conway2.cells) == 4, "Two Conway steps should preserve tub"

    # Same initial state, same first step, different second step → different result
    assert not np.array_equal(grid.cells, grid_conway2.cells), (
        "Different second rule should produce different result"
    )


def test_step_forward_pushes_history():
    """step_forward saves current state to history before evolving."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(1, 1, True)
    assert len(grid.history) == 0

    grid.current_rule = CONWAY
    grid.step_forward()

    assert len(grid.history) == 1, "History should contain 1 entry after step_forward"


def test_step_back_restores_previous_state():
    """step_back restores the grid state from before step_forward."""
    grid = Grid(rows=5, cols=5)
    for r, c in [(2, 1), (2, 2), (2, 3)]:
        grid.set_cell(r, c, True)

    state_before = grid.cells.copy()
    grid.step_forward()
    state_after = grid.cells.copy()

    assert not np.array_equal(state_before, state_after), (
        "Blinker should change after step"
    )

    result = grid.step_back()
    assert result is True, "step_back should return True when history is non-empty"
    assert np.array_equal(grid.cells, state_before), (
        "Grid should be restored to pre-step state"
    )


def test_step_back_empty_history():
    """step_back on empty history returns False and leaves grid unchanged."""
    grid = Grid(rows=5, cols=5)
    grid.set_cell(0, 0, True)

    result = grid.step_back()
    assert result is False, "step_back should return False on empty history"
    assert grid.get_cell(0, 0) is True, "Grid should be unchanged"


def test_multiple_step_forward_then_back():
    """Multiple step_forward followed by step_back restores correct intermediate states."""
    grid = Grid(rows=5, cols=5)
    for r, c in [(2, 1), (2, 2), (2, 3)]:
        grid.set_cell(r, c, True)

    for _ in range(3):
        grid.step_forward()

    # After 3 steps (gen 3): horizontal
    assert grid.get_cell(1, 2) is True
    assert grid.get_cell(2, 1) is False

    # Step back once → gen 2 (vertical)
    grid.step_back()
    assert grid.get_cell(2, 1) is True

    # Step back once more → gen 1 (horizontal)
    grid.step_back()
    assert grid.get_cell(1, 2) is True

    # Step back once more → gen 0 (vertical, initial state)
    grid.step_back()
    assert grid.get_cell(2, 1) is True


def test_step_forward_back_cycle_repeatable():
    """Grid can evolve again after a forward/back cycle."""
    grid = Grid(rows=5, cols=5)
    for r, c in [(2, 1), (2, 2), (2, 3)]:
        grid.set_cell(r, c, True)

    # Forward then back
    grid.step_forward()
    grid.step_back()

    assert grid.get_cell(2, 1) is True

    grid.step_forward()
    assert grid.get_cell(1, 2) is True


def test_rule_switch_conway_vs_day_night():
    """Pattern stable under Conway dies under Day & Night (S34678 excludes 2)."""
    grid = Grid(rows=7, cols=7)
    # Tub pattern: each live cell has exactly 2 neighbors
    tub_cells = [(3, 2), (2, 3), (3, 4), (4, 3)]
    for r, c in tub_cells:
        grid.set_cell(r, c, True)

    grid.apply_rule()
    for r, c in tub_cells:
        assert grid.get_cell(r, c) is True, "Tub cell should survive under Conway"

    grid2 = Grid(rows=7, cols=7)
    grid2.current_rule = DAY_NIGHT
    for r, c in tub_cells:
        grid2.set_cell(r, c, True)
    grid2.apply_rule()
    assert np.sum(grid2.cells) == 0, "Tub should die under Day & Night"

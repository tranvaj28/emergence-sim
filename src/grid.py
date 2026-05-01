"""
Grid state management for cellular automata simulation.
Includes toroidal neighbor counting and history buffer.
"""

import numpy as np
from collections import deque
from typing import Optional

from . import config
from .rules import CONWAY, RuleSet


class HistoryBuffer:
    """FIFO buffer that stores copies of Grid states for rewind support."""

    def __init__(self, maxlen: int = None):
        if maxlen is None:
            maxlen = config.MAX_HISTORY
        self.maxlen = maxlen
        self._deque = deque(maxlen=maxlen)

    def push(self, grid: "Grid") -> None:
        self._deque.append((grid.cells.copy(), grid.rows, grid.cols))

    def pop(self) -> Optional["Grid"]:
        if not self._deque:
            return None
        cells, rows, cols = self._deque.pop()
        g = Grid(rows=rows, cols=cols)
        g.cells = cells
        return g

    def clear(self) -> None:
        self._deque.clear()

    def __len__(self) -> int:
        return len(self._deque)


class Grid:
    """Represents a cellular automaton grid with toroidal wrapping."""

    def __init__(self, rows: int = None, cols: int = None):
        """
        Initialize a grid with all dead cells.

        Args:
            rows: Number of rows (defaults to config.GRID_SIZE).
            cols: Number of columns (defaults to config.GRID_SIZE).
        """
        if rows is None:
            rows = config.GRID_SIZE
        if cols is None:
            cols = config.GRID_SIZE

        self.rows = rows
        self.cols = cols
        # Boolean array: True = alive, False = dead
        self.cells = np.zeros((rows, cols), dtype=bool)

        # History buffer for rewind functionality
        self.history = HistoryBuffer()

        # Current rule set applied when stepping forward
        self._current_rule = CONWAY

    @property
    def current_rule(self) -> RuleSet:
        return self._current_rule

    @current_rule.setter
    def current_rule(self, rule: RuleSet) -> None:
        if rule is not self._current_rule:
            self._current_rule = rule
            self.history.clear()

    def neighbor_counts(self) -> np.ndarray:
        """
        Compute the number of alive neighbors for each cell using toroidal wrap.

        Uses numpy.roll to create shifted views of the grid in all 8 directions
        and sums them to produce neighbor counts.

        Returns:
            2D integer array of neighbor counts (0‑8).
        """
        counts = np.zeros((self.rows, self.cols), dtype=int)

        # Define all 8 Moore neighborhood directions as (dy, dx)
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),  # top row
            (0, -1),
            (0, 1),  # middle row (skip self)
            (1, -1),
            (1, 0),
            (1, 1),  # bottom row
        ]

        for dy, dx in directions:
            # Shift grid by (dy, dx) with toroidal wrap
            shifted = np.roll(self.cells, shift=(dy, dx), axis=(0, 1))
            counts += shifted

        return counts

    def apply_rule(self, rule: Optional[RuleSet] = None) -> None:
        """
        Apply a cellular automaton rule to the grid, advancing one generation.

        Args:
            rule: The rule set to apply. Uses self.current_rule if not provided.
        """
        if rule is not None:
            self._current_rule = rule
        neighbor_counts = self.neighbor_counts()

        r = self.current_rule
        born_mask = ~self.cells & np.isin(neighbor_counts, list(r.born))
        survive_mask = self.cells & np.isin(neighbor_counts, list(r.survive))
        self.cells = born_mask | survive_mask

    def get_cell(self, row: int, col: int) -> bool:
        """Return the state of the cell at (row, col)."""
        return bool(self.cells[row, col])

    def set_cell(self, row: int, col: int, alive: bool) -> None:
        """Set the state of the cell at (row, col)."""
        self.cells[row, col] = alive

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle the state of the cell at (row, col)."""
        self.cells[row, col] = not self.cells[row, col]

    def clear(self) -> None:
        """Set all cells to dead (False)."""
        self.cells.fill(False)
        self.history.clear()

    def clear_history(self) -> None:
        """Clear the history buffer without affecting the current grid."""
        self.history.clear()

    def randomize(self, density: float = config.RANDOM_DENSITY) -> None:
        """
        Randomly set cells to alive with given probability.

        Args:
            density: Probability (0‑1) that a cell is alive (default from config).
        """
        self.cells = np.random.random((self.rows, self.cols)) < density
        self.history.clear()

    def copy(self) -> "Grid":
        """Return a deep copy of this grid."""
        new_grid = Grid(self.rows, self.cols)
        new_grid.cells = self.cells.copy()
        # History is not copied (new grid starts with empty history)
        return new_grid

    def push_to_history(self) -> None:
        """Save the current grid state to the history buffer."""
        self.history.push(self)

    def pop_from_history(self) -> Optional[np.ndarray]:
        """
        Restore the most recent grid state from history buffer.

        Returns:
            The restored grid state (numpy array) if history not empty,
            otherwise None.
        """
        previous = self.history.pop()
        if previous is None:
            return None
        self.cells = previous.cells
        return self.cells

    def step_forward(self, rule: Optional[RuleSet] = None) -> None:
        """
        Advance the grid by one generation, preserving current state in history.

        Args:
            rule: The rule set to apply. Uses self.current_rule if not provided.
        """
        self.push_to_history()
        self.apply_rule(rule)

    def step_back(self) -> bool:
        """
        Step backward one generation, restoring the previous grid state from history.

        If history is empty, does nothing.

        Returns:
            True if a previous state was restored, False if history was empty.
        """
        return self.pop_from_history() is not None

    def __str__(self) -> str:
        """Return a string representation of the grid."""
        alive_count = np.sum(self.cells)
        return f"Grid({self.rows}×{self.cols}, alive={alive_count}, history={len(self.history)})"

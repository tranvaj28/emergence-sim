"""Unit tests for HUD and Statistics classes."""

from src import config
from src.grid import Grid
from src.hud import Statistics


def test_statistics_initial_values():
    """Statistics starts with zero live_count and 0.0 percentage."""
    stats = Statistics()
    assert stats.live_count == 0
    assert stats.live_percentage == 0.0
    assert len(stats.population_history) == 0


def test_statistics_update_counts():
    """Updating with a grid calculates correct live_count."""
    stats = Statistics()
    grid = Grid(rows=10, cols=10)
    grid.set_cell(0, 0, True)
    grid.set_cell(5, 5, True)
    grid.set_cell(9, 9, True)
    stats.update(grid)
    assert stats.live_count == 3


def test_statistics_live_percentage():
    """live_percentage = live_count / total_cells."""
    stats = Statistics()
    grid = Grid(rows=10, cols=10)
    for r in range(10):
        for c in range(10):
            if (r + c) % 2 == 0:
                grid.set_cell(r, c, True)
    stats.update(grid)
    expected = 50 / 100
    assert stats.live_percentage == expected


def test_statistics_update_replaces_counts():
    """Calling update again recalculates from the new grid."""
    stats = Statistics()
    grid = Grid(rows=5, cols=5)

    grid.set_cell(0, 0, True)
    stats.update(grid)
    assert stats.live_count == 1

    grid.set_cell(1, 1, True)
    grid.set_cell(2, 2, True)
    stats.update(grid)
    assert stats.live_count == 3


def test_population_history_records_on_update():
    """population_history appends live_count each time update is called."""
    stats = Statistics()
    grid = Grid(rows=10, cols=10)

    grid.set_cell(0, 0, True)
    stats.update(grid)
    assert stats.population_history == [1]

    grid.set_cell(1, 1, True)
    stats.update(grid)
    assert stats.population_history == [1, 2]

    grid.set_cell(2, 2, True)
    stats.update(grid)
    assert stats.population_history == [1, 2, 3]


def test_population_history_maxlen():
    """population_history is a circular buffer with maxlen=GRAPH_HISTORY."""
    stats = Statistics()
    grid = Grid(rows=10, cols=10)

    for i in range(config.GRAPH_HISTORY + 50):
        grid.set_cell(0, 0, bool(i % 2))
        stats.update(grid)

    assert len(stats.population_history) == config.GRAPH_HISTORY


def test_population_history_fifo():
    """When full, oldest entries are discarded (FIFO)."""
    stats = Statistics()
    grid = Grid(rows=10, cols=10)

    for i in range(config.GRAPH_HISTORY + 10):
        grid.set_cell(0, 0, bool(i % 2))
        stats.update(grid)

    # The oldest 10 entries should be gone; first remaining entry is index 10
    first_remaining = stats.population_history[0]
    grid2 = Grid(rows=10, cols=10)
    grid2.set_cell(0, 0, bool(10 % 2))
    stats2 = Statistics()
    stats2.update(grid2)
    assert first_remaining == stats2.population_history[0], (
        "First entry after FIFO discard should match generation 10"
    )

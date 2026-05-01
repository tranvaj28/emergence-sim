"""
HUD (Heads-Up Display) for cellular automata simulator.
Shows generation count, play/pause status, and other simulation info.
"""

from collections import deque

import numpy as np
import pygame

from . import config


class Statistics:
    """Tracks population statistics over the simulation lifetime."""

    def __init__(self):
        self.live_count = 0
        self.live_percentage = 0.0
        self._history = deque(maxlen=config.GRAPH_HISTORY)

    def update(self, grid) -> None:
        """Recalculate statistics from the current grid state."""
        total = grid.rows * grid.cols
        self.live_count = int(np.sum(grid.cells))
        self.live_percentage = self.live_count / total
        self._history.append(self.live_count)

    @property
    def population_history(self):
        return list(self._history)

    def clear_history(self) -> None:
        self._history.clear()


class HUD:
    """Heads-up display overlay for simulation statistics."""

    def __init__(self):
        """Initialize HUD resources."""
        self.font = pygame.font.Font(None, 24)
        self._graph_surface = pygame.Surface((config.GRAPH_WIDTH, config.GRAPH_HEIGHT))

    def draw_graph(
        self,
        screen: pygame.Surface,
        population_history: list,
        dest_x: int,
        dest_y: int,
    ) -> None:
        """Render population history as a line graph on a dedicated surface.

        Args:
            screen: Pygame surface to draw on.
            population_history: List of live counts per generation.
            dest_x: X position to blit the graph.
            dest_y: Y position to blit the graph.
        """
        self._graph_surface.fill(config.COLOR_HUD_BG)
        pygame.draw.rect(
            self._graph_surface,
            config.COLOR_HUD_TEXT,
            self._graph_surface.get_rect(),
            1,
        )

        if len(population_history) >= 2:
            w = config.GRAPH_WIDTH
            h = config.GRAPH_HEIGHT
            total_cells = config.GRID_SIZE * config.GRID_SIZE
            n = len(population_history)
            points = []
            for i, count in enumerate(population_history):
                x = int(i * w / max(1, n - 1))
                y = h - int(count * h / total_cells)
                points.append((x, y))
            pygame.draw.lines(
                self._graph_surface, config.COLOR_GRAPH_LINE, False, points, 1
            )

        screen.blit(self._graph_surface, (dest_x, dest_y))

    def draw(
        self,
        screen: pygame.Surface,
        generation: int,
        playing: bool,
        speed: int,
        rule_name: str,
        population_history: list = None,
        live_count: int = None,
        live_percentage: float = None,
    ) -> None:
        """
        Draw the HUD onto the given screen surface.

        Args:
            screen: Pygame surface to draw on.
            generation: Current generation number.
            playing: Whether simulation is playing (True) or paused (False).
            speed: Simulation speed in steps per second.
            rule_name: Name of the current rule set.
            population_history: List of live counts per generation for graph.
            live_count: Number of alive cells.
            live_percentage: Fraction of alive cells (0-1).
        """
        hud_top = config.GRID_SIZE * config.CELL_SIZE
        hud_rect = pygame.Rect(0, hud_top, config.WINDOW_WIDTH, config.HUD_HEIGHT)
        pygame.draw.rect(screen, config.COLOR_HUD_BG, hud_rect)

        play_status = "PLAYING" if playing else "PAUSED"

        lines = [
            f"Generation: {generation}",
            f"Status: {play_status}",
            f"Speed: {speed} steps/sec",
            f"Rule: {rule_name}",
        ]
        if live_count is not None and live_percentage is not None:
            pct = live_percentage * 100
            lines.append(f"Population: {live_count} ({pct:.1f}%)")

        y_offset = hud_top + config.HUD_PADDING
        for line in lines:
            text = self.font.render(line, True, config.COLOR_HUD_TEXT)
            screen.blit(text, (config.HUD_PADDING, y_offset))
            y_offset += text.get_height() + 4

        if population_history is not None:
            graph_x = config.WINDOW_WIDTH - config.GRAPH_WIDTH - config.HUD_PADDING
            graph_y = hud_top + config.HUD_PADDING
            self.draw_graph(screen, population_history, graph_x, graph_y)

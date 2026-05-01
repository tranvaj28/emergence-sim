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

    def draw(
        self,
        screen: pygame.Surface,
        generation: int,
        playing: bool,
        speed: int,
        rule_name: str,
    ) -> None:
        """
        Draw the HUD onto the given screen surface.

        Args:
            screen: Pygame surface to draw on.
            generation: Current generation number.
            playing: Whether simulation is playing (True) or paused (False).
            speed: Simulation speed in steps per second.
            rule_name: Name of the current rule set.
        """
        # HUD background
        hud_rect = pygame.Rect(
            0,
            config.GRID_SIZE * config.CELL_SIZE,
            config.WINDOW_WIDTH,
            config.HUD_HEIGHT,
        )
        pygame.draw.rect(screen, config.COLOR_HUD_BG, hud_rect)

        # Prepare text lines
        play_status = "PLAYING" if playing else "PAUSED"

        lines = [
            f"Generation: {generation}",
            f"Status: {play_status}",
            f"Speed: {speed} steps/sec",
            f"Rule: {rule_name}",
        ]

        # Draw each line
        y_offset = config.WINDOW_HEIGHT - config.HUD_HEIGHT + config.HUD_PADDING
        for line in lines:
            text = self.font.render(line, True, config.COLOR_HUD_TEXT)
            screen.blit(text, (config.HUD_PADDING, y_offset))
            y_offset += text.get_height() + 4  # small spacing between lines

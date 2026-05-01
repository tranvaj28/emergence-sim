"""
Main entry point for the cellular automata simulator.
Pygame window initialization and event loop skeleton.
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src import config
from src.grid import Grid
from src.rules import CONWAY, DAY_NIGHT, HIGHLIFE
from src.hud import HUD, Statistics


class Simulation:
    """Main simulation controller."""

    def __init__(self):
        """Initialize Pygame and create window."""
        pygame.init()

        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        )
        pygame.display.set_caption("Emergence Simulator")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create grid (empty for now)
        self.grid = Grid()

        # Simulation state (skeleton)
        self.generation = 0
        self.playing = True  # simulation runs automatically
        self.speed = config.DEFAULT_SPEED  # steps per second
        self.step_accumulator = 0.0  # seconds accumulated toward next step
        self.stats = Statistics()
        self.stats.update(self.grid)
        self.hud = HUD()

    def screen_to_grid(self, x: int, y: int) -> tuple[int, int]:
        """Convert screen coordinates to grid cell indices."""
        col = x // config.CELL_SIZE
        row = y // config.CELL_SIZE
        # Clamp to grid bounds
        row = max(0, min(row, self.grid.rows - 1))
        col = max(0, min(col, self.grid.cols - 1))
        return row, col

    def handle_mouse_click(self, button: int, pos: tuple[int, int]) -> None:
        """Set cell state based on mouse button (left=alive, right=dead)."""
        row, col = self.screen_to_grid(pos[0], pos[1])
        if button == 1:  # left button
            self.grid.set_cell(row, col, True)
        elif button == 3:  # right button
            self.grid.set_cell(row, col, False)

    def handle_events(self):
        """Process Pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.playing = not self.playing
                elif event.key == pygame.K_RIGHT:
                    self.grid.step_forward()
                    self.generation += 1
                    self.stats.update(self.grid)
                elif event.key == pygame.K_LEFT:
                    if self.grid.step_back():
                        self.generation -= 1
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    self.speed = min(self.speed + 1, config.SPEED_RANGE[1])
                elif event.key == pygame.K_MINUS:
                    self.speed = max(self.speed - 1, config.SPEED_RANGE[0])
                elif event.key == pygame.K_1:
                    self.grid.current_rule = CONWAY
                elif event.key == pygame.K_2:
                    self.grid.current_rule = HIGHLIFE
                elif event.key == pygame.K_3:
                    self.grid.current_rule = DAY_NIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.button, event.pos)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0] or event.buttons[2]:  # left or right button held
                    self.handle_mouse_click(event.buttons[0] and 1 or 3, event.pos)

    def update(self, dt: float = 0.0):
        """Update simulation state.

        Args:
            dt: Time elapsed since last update in seconds.
        """
        if not self.playing:
            return

        # Accumulate time toward next step
        self.step_accumulator += dt

        # Calculate time per step based on speed (steps per second)
        time_per_step = 1.0 / self.speed

        while self.step_accumulator >= time_per_step:
            self.grid.step_forward()
            self.generation += 1
            self.step_accumulator -= time_per_step
            self.stats.update(self.grid)

    def draw(self):
        """Draw the grid and HUD."""
        # Clear screen
        self.screen.fill(config.COLOR_BACKGROUND)

        # Draw grid cells
        for row in range(self.grid.rows):
            for col in range(self.grid.cols):
                color = (
                    config.COLOR_ALIVE
                    if self.grid.get_cell(row, col)
                    else config.COLOR_DEAD
                )
                rect = pygame.Rect(
                    col * config.CELL_SIZE,
                    row * config.CELL_SIZE,
                    config.CELL_SIZE,
                    config.CELL_SIZE,
                )
                pygame.draw.rect(self.screen, color, rect)

        # Draw grid lines (optional, can be toggled later)
        if config.COLOR_GRID:
            # Vertical lines
            for col in range(self.grid.cols + 1):
                x = col * config.CELL_SIZE
                pygame.draw.line(
                    self.screen,
                    config.COLOR_GRID,
                    (x, 0),
                    (x, config.GRID_SIZE * config.CELL_SIZE),
                    1,
                )
            # Horizontal lines
            for row in range(self.grid.rows + 1):
                y = row * config.CELL_SIZE
                pygame.draw.line(
                    self.screen,
                    config.COLOR_GRID,
                    (0, y),
                    (config.GRID_SIZE * config.CELL_SIZE, y),
                    1,
                )

        # Draw HUD
        self.hud.draw(
            self.screen,
            self.generation,
            self.playing,
            self.speed,
            self.grid.current_rule.name,
        )

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            dt = self.clock.tick(config.FPS) / 1000.0  # seconds
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
    main()

"""
Configuration constants for the cellular automata simulator.
"""

# Grid dimensions
GRID_SIZE = 100  # 100×100 grid
CELL_SIZE = 8  # pixels per cell
TOROIDAL = True  # wrap edges

# Window dimensions
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 100  # extra space for HUD
FPS = 60  # target frames per second

# Simulation settings
SPEED_RANGE = (1, 60)  # steps per second (min, max)
DEFAULT_SPEED = 10  # initial simulation speed

# History buffer
MAX_HISTORY = 500  # maximum generations stored for rewind
GRAPH_HISTORY = 200  # generations displayed in population graph

# Colors (RGB tuples)
COLOR_ALIVE = (255, 255, 255)  # white
COLOR_DEAD = (0, 0, 0)  # black
COLOR_GRID = (40, 40, 40)  # dark gray
COLOR_BACKGROUND = (10, 10, 20)  # dark blue‑black
COLOR_HUD_TEXT = (220, 220, 220)  # light gray
COLOR_GRAPH_LINE = (0, 255, 255)  # cyan
COLOR_HUD_BG = (20, 20, 30)  # slightly lighter than background

# HUD layout
HUD_HEIGHT = 100
HUD_PADDING = 10
GRAPH_WIDTH = 200
GRAPH_HEIGHT = 60

# Random seed density (percentage of alive cells)
RANDOM_DENSITY = 0.3  # 30%

# Convenience collections
COLORS = {
    "alive": COLOR_ALIVE,
    "dead": COLOR_DEAD,
    "grid": COLOR_GRID,
    "background": COLOR_BACKGROUND,
    "hud_text": COLOR_HUD_TEXT,
    "graph_line": COLOR_GRAPH_LINE,
    "hud_bg": COLOR_HUD_BG,
}

# Research: Desktop Cellular Automata Simulator

## Unknowns & Decisions

### 1. PyGame Version Compatibility
**Unknown**: Which PyGame 2.x version is stable with Python 3.11+?
**Research**: Check PyGame documentation and recent releases.
**Decision**: Use PyGame 2.5.0 (latest stable as of 2026‑04‑10).

### 2. SciPy Dependency
**Unknown**: Is SciPy required for convolve2d, or can we implement manual neighbor sum using numpy rolls?
**Research**: Evaluate performance of manual sum vs scipy.signal.convolve2d for 100×100 grid.
**Decision**: Implement manual neighbor sum using numpy rolls to avoid external dependency; benchmark.

### 3. Performance Optimization
**Unknown**: How to achieve 60 fps while stepping up to 60 steps per second?
**Research**: Profile grid update and rendering loops; consider double buffering, limiting redraws.
**Decision**: Use numpy boolean arrays for grid; compute next generation via vectorized neighbor sum; limit redraws to changed cells.

### 4. History Buffer Implementation
**Unknown**: How to store 500 generations of 100×100 boolean arrays efficiently?
**Research**: Evaluate memory usage of deque of numpy arrays vs list of flattened arrays.
**Decision**: Use collections.deque(maxlen=500) storing numpy bool arrays (≈10 KB each, total ≈5 MB).

### 5. Graph Rendering
**Unknown**: How to render a simple line graph of population over 200 generations in PyGame?
**Research**: Look at PyGame drawing primitives; consider rendering to a small surface.
**Decision**: Draw line graph using pygame.draw.lines on a dedicated surface, scaled to fit HUD area.

### 6. Keyboard Shortcuts
**Unknown**: How to handle keyboard shortcuts while maintaining responsive simulation?
**Research**: PyGame event queue handling; differentiate between held and pressed keys.
**Decision**: Use pygame.KEYDOWN events for single‑press actions (space, arrows, number keys).

### 7. Toroidal Neighbor Calculation
**Unknown**: Efficient method to compute neighbor counts with wrap‑around.
**Research**: Compare numpy.roll along both axes vs manual indexing.
**Decision**: Use numpy.roll to create shifted views and sum them.

## Technology Choices
- Python 3.11+
- PyGame 2.5.0
- NumPy 1.24+
- No SciPy (initially)
- pytest for testing
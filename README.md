# Mondrian Tiling Solver

An AI-powered solver for the Mondrian Art Problem using informed search algorithms. This project finds optimal tilings of a square grid into distinct rectangles, minimizing the difference between the largest and smallest rectangle areas.

## Problem Description

The **Mondrian Art Problem** is a combinatorial optimization challenge inspired by the geometric abstract art of Piet Mondrian. Given a square grid of size `a × a`, the goal is to:

1. Partition the square into rectangles with distinct dimensions
2. Minimize the **Mondrian score**: the difference between the largest and smallest rectangle areas
3. Ensure no two rectangles share the same dimensions (even if rotated)

### Example Solution

For a 5×5 grid:

- **Valid tiling**: Rectangles with dimensions {2×3, 1×4, 2×5, 1×3, 1×1}
- **Mondrian score**: max_area - min_area = 10 - 1 = 9
- **Invalid**: Two rectangles both sized 2×3

## Algorithm

This solver uses a **best-first search** approach with three key operations:

### Operations

1. **Split**: Divide a rectangle into two smaller rectangles
2. **Merge**: Combine two adjacent rectangles into one larger rectangle
3. **Merge-Split**: Merge two L-shaped adjacent rectangles and split the result

### Search Strategy

- **State representation**: A configuration of rectangles with a score (max_area - min_area)
- **Priority queue**: States sorted by score (best scores explored first)
- **Depth limiting**: Prevents infinite search depth
- **Queue size limiting**: Maintains only the most promising states
- **Duplicate detection**: Avoids re-exploring identical states

### Key Features

- Random initial state generation with multiple iterations
- Validation to ensure all rectangles have unique dimensions
- Optimized adjacency detection for efficient merge operations
- Visual representation using Tkinter

## Installation

### Requirements

- Python 3.x
- Tkinter (usually included with Python)

### Setup

```bash
git clone https://github.com/LewisTrundle/Mondrian-Tiling.git
cd Mondrian-Tiling
```

No additional dependencies are required beyond Python's standard library.

## Usage

### Basic Usage

```python
python mondrian_tiles.py
```

By default, this solves a 12×12 grid with the following parameters:

- Grid size: 12×12
- Max depth: 10
- Max queue size: 20
- Random iterations: 25

### Customizing Parameters

Modify the final line in `mondrian_tiles.py`:

```python
SolveMondrian(a, max_depth, max_size, ran_iterations)
```

**Parameters:**

- `a`: Size of the square grid (e.g., 12 for 12×12)
- `max_depth`: Maximum search depth (higher = more thorough but slower)
- `max_size`: Maximum priority queue size (higher = more memory but better solutions)
- `ran_iterations`: Number of random initial states to try (higher = better chance of optimal solution)

### Examples

```python
# Solve a 10x10 grid with aggressive search
SolveMondrian(10, 15, 30, 50)

# Solve a smaller 8x8 grid quickly
SolveMondrian(8, 8, 15, 20)
```

## Output

The program outputs:

1. **Console**: Best state score, depth, evaluation value, and number of tiles
2. **GUI Window**: Visual representation of the solution with:
   - Red rectangles showing the tiling
   - Area values displayed in each rectangle
   - Final Mondrian score

Example output:

```text
Best state:    score:  8  depth:  5  eval:  13  no. of tiles:  9
```

## Implementation Details

### Core Classes

- **`Rectangle`**: Represents a single rectangle with coordinates, width, height, and area
- **`State`**: Represents a tiling configuration with tiles, score, and depth
- **`Mondrian`**: Manages the priority queue and explored states
- **`Coord`**: Helper class for coordinate management

### Key Functions

- **`create_initial_state(a)`**: Generates a random valid initial tiling
- **`optimise(init_state, maxdepth, maxsize)`**: Performs best-first search
- **`split(state)`**: Splits a rectangle to improve the score
- **`merge(state)`**: Merges adjacent rectangles
- **`merge_split(state)`**: Advanced operation combining merge and split
- **`validate(l, b, state)`**: Ensures rectangle dimensions are unique
- **`drawMondrian(state, a)`**: Visualizes the solution

## Performance Considerations

- **Small grids (≤ 10×10)**: Fast, typically finds good solutions in seconds
- **Medium grids (11×14)**: Moderate runtime, may take minutes for optimal solutions
- **Large grids (≥ 15×15)**: Can be slow; consider reducing max_depth or max_size

### Optimization Tips

1. Increase `ran_iterations` for better solutions (at cost of runtime)
2. Increase `max_depth` for more thorough exploration
3. Increase `max_size` to keep more candidate states in memory
4. Balance all three parameters based on available time/resources

## Example Solutions

For common grid sizes, typical achievable scores:

| Grid Size | Typical Best Score | Tiles |
|-----------|-------------------|-------|
| 5×5       | 5-9               | 5-7   |
| 8×8       | 6-12              | 7-10  |
| 10×10     | 8-15              | 9-12  |
| 12×12     | 8-18              | 10-14 |

> **Note:** Scores vary based on random initial states and search parameters

## Limitations

- No guarantee of finding the absolute optimal solution (heuristic search)
- Performance degrades for very large grids (> 15×15)
- Memory usage increases with `max_size` parameter

## License

This project is open source and available for educational purposes.

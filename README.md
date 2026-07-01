
<p align="center">
  <img src="https://github.com/mirr-x/42-CC-1337/blob/main/images/amazeing_.png" alt="get_next_line banner">
</p>


<img src="https://github.com/mirr-x/42-CC-1337/blob/main/gif/amazing.gif" alt="42 Porto Common Core Banner" />


*This project has been created as part of the 42 curriculum by bdebbagh, molahrech.*

## Description
A-Maze-ing is a Python maze generator that reads a config file, generates a random maze,
adds a visible "42" pattern when size allows, and writes the maze to a hexadecimal wall
format file. The project also provides an interactive terminal rendering to regenerate the
maze, show/hide the shortest path, animate the solution, and rotate wall colors.

The mandatory requirements covered are:
- Config-driven generation (`WIDTH`, `HEIGHT`, `ENTRY`, `EXIT`, `OUTPUT_FILE`,
  `PERFECT`, optional `SEED`)
- Output format with hexadecimal walls, then a blank line, then entry, exit, and shortest
  path (`N`, `E`, `S`, `W`)
- Reusable maze generation module in `mazegen/`
- Graceful error handling for invalid input and file issues

## Instructions
### Requirements
- Python 3.10+
- `flake8`
- `mypy`

### Install dependencies
```bash
make install
```

### Run
```bash
python3 a_maze_ing.py config.txt
```
or
```bash
make run
```

### Debug
```bash
make debug
```

### Lint and type-check
```bash
make lint
```
Optional strict mode:
```bash
make lint-strict
```

### Clean caches
```bash
make clean
```

## Configuration File Format
Each non-empty line is `KEY=VALUE`. Lines starting with `#` are ignored.
Inline comments after values are accepted.

Mandatory keys:
- `WIDTH`: maze width in cells
- `HEIGHT`: maze height in cells
- `ENTRY`: `x,y` coordinates of entry cell
- `EXIT`: `x,y` coordinates of exit cell
- `OUTPUT_FILE`: output maze filename
- `PERFECT`: `True` or `False`

Optional keys:
- `SEED`: integer random seed for reproducible generation

Example:
```txt
WIDTH=15
HEIGHT=13
ENTRY=0,0
EXIT=14,12
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

## Maze Generation Algorithm
### Chosen algorithm
Iterative DFS (depth-first search) with backtracking is used to build a spanning-tree maze.

### Why this algorithm
- Simple and reliable to implement
- Produces valid connected mazes
- Efficient for the project scale
- Easy to extend with optional extra openings for non-perfect mazes

### PERFECT behavior
- `PERFECT=True`: DFS tree only (single unique path between any two connected cells)
- `PERFECT=False`: DFS tree + extra wall openings to introduce loops

## Reusable Module
Reusable code is located in `mazegen/`:
- `mazegen/maze.py`: generation, solving, serialization
- `mazegen/draw_maze.py`: terminal rendering and animation
- `mazegen/types.py`: shared type aliases

Basic usage example:
```python
from mazegen import Maze_

maze = Maze_("config.txt")
maze.build_grid()
maze.build_maze()
path = maze.solve_bfs()
maze.save_to_file()
```

The generated internal structure is a 2D grid of cells where each cell stores wall states
(`N`, `E`, `S`, `W`) and a `visited` flag.

## Team and Project Management
### Roles
- bdebbagh_molahrech: architecture, maze generation logic, config parsing, rendering,
  output format, lint/type-check compliance

### Planning and evolution
- Initial phase: parser + base DFS generation
- Middle phase: visual rendering + interactions + BFS shortest path
- Final phase: output format compliance, documentation, lint/type-check hardening

### What worked well
- Clear separation between generation (`maze.py`) and rendering (`draw_maze.py`)
- Iterative implementation with regular lint/type-check validation

### What could be improved
- Add unit tests for parser and format serialization
- Add validation script integration in CI
- Add second generation algorithm as bonus

### Tools used
- Python 3.10+
- flake8
- mypy
- Make

## Resources
- Python docs: https://docs.python.org/3/
- PEP 8: https://peps.python.org/pep-0008/
- PEP 257: https://peps.python.org/pep-0257/
- BFS reference: https://en.wikipedia.org/wiki/Breadth-first_search
- DFS maze generation reference: https://en.wikipedia.org/wiki/Maze_generation_algorithm

### AI usage
AI assistance was used for:
- Reviewing specification compliance against the subject
- Suggesting refactors for output formatting and coordinate conventions
- Identifying missing documentation and consistency issues

All generated suggestions were reviewed, tested, and adapted manually before keeping
changes in the project.

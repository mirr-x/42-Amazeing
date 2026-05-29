from typing import Protocol
import sys
from .types import Coord
import time


class MazeLike(Protocol):
    """Minimal maze interface needed by the renderer."""

    width: int
    height: int
    entry: Coord
    exit: Coord
    grid: list[list[dict[str, bool]]]


class DrawMaze:
    """Render and animate the maze in the terminal."""

    RESET = "\033[0m"
    WHITE = "\033[97m"           # wall       → white ██
    BLACK = "\033[30m"           # passage    → black ██
    GRAY = "\033[38;5;145m"     # 42 cells   → gray ██  (38 = foreground)
    PURPLE = "\033[95m"           # entry      → purple ██
    RED = "\033[91m"           # exit       → red ██
    BLOCK = "██"
    BALL = "[]"
    _first_draw = True
    COLORS = [
        "\033[97m",   # white
        "\033[93m",   # yellow
        "\033[92m",   # green
        "\033[96m",   # cyan
        "\033[94m",   # blue
        "\033[91m",   # red
    ]
    _color_index = 0

    def rotate_color(self) -> None:
        """Cycle to the next wall color."""
        self._color_index = (self._color_index + 1) % len(self.COLORS)
        self.WHITE = self.COLORS[self._color_index]

    def __init__(self, maze: MazeLike) -> None:
        """Store maze reference used by all draw operations."""
        self.maze = maze

    def _is_42_cell(self, y: int, x: int) -> bool:
        """42 cell = visited True + ALL 4 walls still True."""
        c = self.maze.grid[y][x]
        return c["visited"] and c["N"] and c["E"] and c["S"] and c["W"]

    def _build_render_grid(self) -> list[list[bool]]:
        """Build a wall/passage matrix used by terminal rendering."""
        h = self.maze.height
        w = self.maze.width
        render = [[True] * (w * 2 + 1) for _ in range(h * 2 + 1)]

        for y in range(h):
            for x in range(w):
                ry = y * 2 + 1
                rx = x * 2 + 1
                cell = self.maze.grid[y][x]

                if self._is_42_cell(y, x):
                    render[ry][rx] = False
                    continue

                render[ry][rx] = False
                if not cell["N"]:
                    render[ry - 1][rx] = False
                if not cell["S"]:
                    render[ry + 1][rx] = False
                if not cell["W"]:
                    render[ry][rx - 1] = False
                if not cell["E"]:
                    render[ry][rx + 1] = False

        return render

    def draw_maze(
            self,
            current_cell: Coord,
            path: list[Coord] | None = None) -> None:
        """Draw maze — white walls, black passages, gray 42, red path ⚽."""
        if self._first_draw:
            sys.stdout.write("\033[2J")
            self._first_draw = False
        sys.stdout.write("\033[H")

        h = self.maze.height
        w = self.maze.width
        render = self._build_render_grid()

        path = path if path else []

        for ry in range(h * 2 + 1):
            line = ""

            for rx in range(w * 2 + 1):
                # WALL
                if render[ry][rx]:
                    line += self.WHITE + self.BLOCK + self.RESET
                    continue
                # CENTER CELL
                is_center = (ry % 2 == 1) and (rx % 2 == 1)

                if is_center:
                    cy = (ry - 1) // 2
                    cx = (rx - 1) // 2

                    if (cy, cx) == current_cell:
                        line += self.PURPLE + self.BLOCK + self.RESET
                    elif (cy, cx) in path:
                        line += self.PURPLE + self.BLOCK + self.RESET
                    elif (cy, cx) == self.maze.entry:
                        line += self.PURPLE + self.BLOCK + self.RESET
                    elif (cy, cx) == self.maze.exit:
                        line += self.RED + self.BLOCK + self.RESET
                    elif self._is_42_cell(cy, cx):
                        line += self.GRAY + self.BLOCK + self.RESET
                    else:
                        line += self.BLACK + self.BLOCK + self.RESET
                # PASSAGES (between cells)
                else:
                    line += self.BLACK + self.BLOCK + self.RESET
            sys.stdout.write(line + "\n")

        sys.stdout.flush()

    def animate_path(
        self,
        path: list[Coord],
        delay: float = 0.008,
    ) -> None:
        """Animate a path by progressively revealing its cells."""
        sys.stdout.write("\033[?25l")
        try:
            for i in range(1, len(path) + 1):
                self.draw_maze(path[i - 1], path[:i])
                time.sleep(delay)
        finally:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()

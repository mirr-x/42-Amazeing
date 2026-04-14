from typing import Protocol
import os
from .types import Coord


class MazeLike(Protocol):
    width: int
    height: int
    entry: Coord
    exit: Coord
    grid: list[list[dict[str, bool]]]


class DrawMaze:
    RESET  = "\033[0m"
    WHITE  = "\033[97m"           # wall       → white ██
    BLACK  = "\033[30m"           # passage    → black ██
    GRAY   = "\033[38;5;145m"     # 42 cells   → gray ██  (38 = foreground)
    PURPLE = "\033[95m"           # entry      → purple ██
    RED    = "\033[91m"           # exit       → red ██
<<<<<<< HEAD
=======
    GREEN  = "\033[92m"           # BFS path   → green ██
>>>>>>> 4578e57 (solve_pfs)
    BLOCK  = "██"
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
        self.maze = maze

    def _is_42_cell(self, y: int, x: int) -> bool:
        """42 cell = visited True + ALL 4 walls still True."""
        c = self.maze.grid[y][x]
        return c["visited"] and c["N"] and c["E"] and c["S"] and c["W"]

    def _build_render_grid(self) -> list[list[bool]]:
        h = self.maze.height
        w = self.maze.width
        render = [[True] * (w * 2 + 1) for _ in range(h * 2 + 1)]

        for y in range(h):
            for x in range(w):
                ry = y * 2 + 1
                rx = x * 2 + 1
                cell = self.maze.grid[y][x]
<<<<<<< HEAD

                if self._is_42_cell(y, x):
                    render[ry][rx] = False
                    if y - 1 >= 0 and self._is_42_cell(y - 1, x):
                        render[ry - 1][rx] = False
                    if y + 1 < h and self._is_42_cell(y + 1, x):
                        render[ry + 1][rx] = False
                    if x - 1 >= 0 and self._is_42_cell(y, x - 1):
                        render[ry][rx - 1] = False
                    if x + 1 < w and self._is_42_cell(y, x + 1):
                        render[ry][rx + 1] = False
                    continue

                render[ry][rx] = False
                if not cell["N"]: render[ry - 1][rx] = False
                if not cell["S"]: render[ry + 1][rx] = False
                if not cell["W"]: render[ry][rx - 1] = False
                if not cell["E"]: render[ry][rx + 1] = False

        return render

    def draw_maze(self, current_cell: Coord) -> None:
        """Draw maze — white walls, black passages, gray 42."""
=======

                if self._is_42_cell(y, x):
                    render[ry][rx] = False
                    if y - 1 >= 0 and self._is_42_cell(y - 1, x):
                        render[ry - 1][rx] = False
                    if y + 1 < h and self._is_42_cell(y + 1, x):
                        render[ry + 1][rx] = False
                    if x - 1 >= 0 and self._is_42_cell(y, x - 1):
                        render[ry][rx - 1] = False
                    if x + 1 < w and self._is_42_cell(y, x + 1):
                        render[ry][rx + 1] = False
                    continue

                render[ry][rx] = False
                if not cell["N"]: render[ry - 1][rx] = False
                if not cell["S"]: render[ry + 1][rx] = False
                if not cell["W"]: render[ry][rx - 1] = False
                if not cell["E"]: render[ry][rx + 1] = False

        return render

    def draw_maze(self, current_cell: Coord, path: list[Coord] | None = None) -> None:
        """Draw maze — white walls, black passages, gray 42, green BFS path."""
>>>>>>> 4578e57 (solve_pfs)
        os.system("clear")
        h = self.maze.height
        w = self.maze.width
        render = self._build_render_grid()
<<<<<<< HEAD
=======
        path_set: set[Coord] = set(path) if path else set()
>>>>>>> 4578e57 (solve_pfs)

        for ry in range(h * 2 + 1):
            line = ""
            for rx in range(w * 2 + 1):
                if render[ry][rx]:
                    line += self.WHITE + self.BLOCK + self.RESET
                else:
                    is_center = (ry % 2 == 1) and (rx % 2 == 1)
                    if is_center:
                        cy = (ry - 1) // 2
                        cx = (rx - 1) // 2
                        if self._is_42_cell(cy, cx):
                            line += self.GRAY + self.BLOCK + self.RESET
                        elif (cy, cx) == self.maze.entry:
                            line += self.PURPLE + self.BLOCK + self.RESET
                        elif (cy, cx) == self.maze.exit:
                            line += self.RED + self.BLOCK + self.RESET
<<<<<<< HEAD
                        else:
                            line += self.BLACK + self.BLOCK + self.RESET
                    else:
=======
                        elif (cy, cx) in path_set:
                            line += self.GREEN + self.BLOCK + self.RESET
                        else:
                            line += self.BLACK + self.BLOCK + self.RESET
                    else:
                        
                        if path_set:
                            py = (ry - 1) // 2 if ry % 2 == 0 else ry // 2
                            px = (rx - 1) // 2 if rx % 2 == 0 else rx // 2
                            if ry % 2 == 0:  
                                c1 = (py, (rx - 1) // 2)
                                c2 = (py + 1, (rx - 1) // 2)
                            else:
                                c1 = ((ry - 1) // 2, px)
                                c2 = ((ry - 1) // 2, px + 1)
                            if c1 in path_set and c2 in path_set:
                                line += self.GREEN + self.BLOCK + self.RESET
                                continue
>>>>>>> 4578e57 (solve_pfs)
                        line += self.BLACK + self.BLOCK + self.RESET
            print(line)
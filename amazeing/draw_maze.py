from typing import Protocol
import os
from .types import Coord


class MazeLike(Protocol):
    width: int
    height: int
    grid: list[list[dict[str, bool]]]


class DrawMaze:
    def __init__(self, maze: MazeLike) -> None:
        self.maze = maze

    def _print_roof(self, cells: int, row: int) -> None:
        for i in range(cells):
            if self.maze.grid[row][i]["N"]:
                print("+---", end="")
            else:
                print("+   ", end="")
        print("+")

    def _print_walls(self, cells: int, row: int, current_cell: Coord) -> None:
        for i in range(cells):
            if self.maze.grid[row][i]["W"]:
                print("|", end="")
            else:
                print(" ", end="")
            if (row, i) == current_cell:
                print(" B ", end="")
            elif self.maze.grid[row][i]["visited"]:
                print(" . ", end="")
            else:
                print("   ", end="")
        if self.maze.grid[row][cells - 1]["E"]:
            print("|")
        else:
            print(" ")

    def _print_last_ground(self, cells: int, row: int):
        for i in range(cells):
            if self.maze.grid[row][i]["S"]:
                print("+---", end="")
            else:
                print("+   ", end="")
        print("+")

    def draw_maze(self, current_cell: Coord) -> None:
        os.system("clear")
        width = self.maze.width
        height = self.maze.height
        for row in range(height):
            self._print_roof(width, row)
            self._print_walls(width, row, current_cell)
            if row == height - 1:
                self._print_last_ground(width, row)

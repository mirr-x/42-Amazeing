from random import choice
import time
from .draw_maze import DrawMaze
from .types import Coord
from enum import Enum


class Config(Enum):
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"
    ENTRY = "ENTRY"
    EXIT = "EXIT"
    OUTPUT_FILE = "OUTPUT_FILE"
    PERFECT = "PERFECT"


class Maze:
    env = "config.txt"

    def __init__(self) -> None:
        """Initialize maze defaults, load config data,
            and validate endpoints.
        """
        self.width: int = 3
        self.height: int = 3
        self.entry: Coord
        self.exit: Coord
        self.output_file: str = "maze.txt"
        self.perfect: bool
        self.grid: list[list[dict[str, bool]]] = []
        self.drawer = DrawMaze(self)
        self._load_env_data()
        self._validate_entry_exit()

    def _load_env_data(self) -> None:
        """ Load data from config.txt to local attrbutes """
        try:
            with open(self.env, "r") as f:
                for line in f:
                    line = ((line.strip()).split("="))
                    if line[0].upper() == Config.WIDTH.value:
                        val = line[1].split()
                        self.width = int(val[0])
                    elif line[0].upper() == Config.HEIGHT.value:
                        val = line[1].split()
                        self.height = int(val[0])
                    elif line[0].upper() == Config.ENTRY.value:
                        val = line[1].split()
                        data = val[0].split(",")
                        self.entry = (int(data[0]), int(data[1]))
                    elif line[0].upper() == Config.EXIT.value:
                        val = line[1].split()
                        data = val[0].split(",")
                        self.exit = (int(data[0]), int(data[1]))
                    elif line[0].upper() == Config.PERFECT.value:
                        val = line[1].split()
                        self.perfect = (
                            True if val[0].upper() == "TRUE" else False)
                    elif line[0].upper() == Config.OUTPUT_FILE.value:
                        val = line[1].split()
                        self.output_file = val[0]
        except FileNotFoundError:
            print("ERROR: file not found")
            exit(1)
        except PermissionError:
            print("ERROR: file permissions")
            exit(1)
        except Exception as e:
            print(f"Unknown ERROR: {e}")
            exit(1)

    def _validate_entry_exit(self) -> None:
        """Validate that entry and exit
            points are within bounds and not equal
        """
        try:
            if not (
                0 <= self.entry[0] < self.height
                and 0 <= self.entry[1] < self.width
            ):
                raise ValueError("Entry point out of bounds")
            if not (
                0 <= self.exit[0] < self.height
                and 0 <= self.exit[1] < self.width
            ):
                raise ValueError("Exit point out of bounds")
            if self.entry == self.exit:
                raise ValueError("Entry must != Exit")
        except ValueError as e:
            print(f"ERROR: Invalid entry/exit coordinates - {e}")
            exit(1)

    def _cell_to_hex(self, cell: Coord) -> str:
        """Convert one cell wall state to a single hexadecimal character."""
        y, x = cell
        val = 0
        cel = self.grid[y][x]
        if cel["N"]:
            val += 1
        if cel["E"]:
            val += 2
        if cel["S"]:
            val += 4
        if cel["W"]:
            val += 8
        return hex(val)[2:].upper()

    def save_to_file(self) -> None:
        """Write the current maze grid to the configured output file."""
        try:
            with open(self.output_file, "w") as f:
                for y in range(self.height):
                    for x in range(self.width):
                        f.write(self._cell_to_hex((y, x)))
                    f.write("\n")
                f.write(f"ENTRY {self.entry[0]},{self.entry[1]}\n")
                f.write(f"EXIT {self.exit[0]},{self.exit[1]}\n")
        except Exception:
            print("save_to_file(): ERROR")

    def build_grid(self) -> None:
        """ Build grid using width and height """
        for _ in range(self.height):
            lis: list[dict[str, bool]] = []
            for _ in range(self.width):
                cell = {
                        "visited": False,
                        "N": True,
                        "E": True,
                        "S": True,
                        "W": True
                    }
                lis.append(cell)
            self.grid.append(lis)

    def print_data(self) -> None:
        """Print config data and dump the grid for debugging purposes."""
        print(f"WIDTH: {self.width}")
        print(f"HEIGHT: {self.height}")
        print(f"ENTRY: {self.entry}")
        print(f"EXIT: {self.exit}")
        print(f"OUTPUT_FILE: {self.output_file}")
        print(f"PERFECT: {self.perfect}")

    def get_neighbors_cells(self, cell: Coord) -> list[Coord]:
        """ Get only neigbors of an cell that are not visited
            return:
                    list of cords (of neigbors)
        """
        neigbors: list[Coord] = []
        y, x = cell
        # check north
        if y - 1 >= 0 and not self.grid[y - 1][x]["visited"]:
            neigbors.append((y - 1, x))
        # check east
        if x + 1 < self.width and not self.grid[y][x + 1]["visited"]:
            neigbors.append((y, x + 1))
        # check south
        if y + 1 < self.height and not self.grid[y + 1][x]["visited"]:
            neigbors.append((y + 1, x))
        # check west
        if x - 1 >= 0 and not self.grid[y][x - 1]["visited"]:
            neigbors.append((y, x - 1))

        return neigbors

    def remove_walls(self, cell1: Coord, cell2: Coord) -> None:
        """ Remove walls bettwen two cells """
        y1, x1 = cell1
        y2, x2 = cell2
        # check North
        if y1 - 1 == y2 and x1 == x2:
            self.grid[y1][x1]["N"] = False
            self.grid[y2][x2]["S"] = False
        # check East
        elif y1 == y2 and x1 + 1 == x2:
            self.grid[y1][x1]["E"] = False
            self.grid[y2][x2]["W"] = False
        # check South
        elif y1 + 1 == y2 and x1 == x2:
            self.grid[y1][x1]["S"] = False
            self.grid[y2][x2]["N"] = False
        # check West
        elif y1 == y2 and x1 - 1 == x2:
            self.grid[y1][x1]["W"] = False
            self.grid[y2][x2]["E"] = False
        else:
            print("Error: Cells dosent much")

    def build_maze(self) -> None:
        """Generate the maze using iterative DFS with backtracking."""
        start = self.entry
        stack: list[Coord] = [start]
        y, x = start
        self.grid[y][x]["visited"] = True
        while stack:
            neighbors = self.get_neighbors_cells(stack[-1])
            self.drawer.draw_maze(stack[-1])
            time.sleep(0.01)
            if neighbors:
                y1, x1 = neighbor = choice(neighbors)
                self.remove_walls(stack[-1], neighbor)
                self.grid[y1][x1]["visited"] = True
                stack.append(neighbor)
            else:
                stack.pop()

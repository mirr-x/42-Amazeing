import json
from random import choice

from .draw_maze import DrawMaze
from .types import Coord

PATTERN_42 = [
    (0, 0),
    (1, 0),
    (2, 0), (2, 1), (2, 2),
    (3, 2),
    (4, 2),
    # digit "2"
    (0, 4), (0, 5), (0, 6),
    (1, 6),
    (2, 4), (2, 5), (2, 6),
    (3, 4),
    (4, 4), (4, 5), (4, 6),
]

class Maze:
    env = "config.txt"
    hex_file = "hex_maze"
    def __init__(self) -> None:
        """Initialize maze defaults, load config data, and validate endpoints."""
        self.width: int = 3
        self.height: int = 3
        self.entry: Coord
        self.exit: Coord
        self.output_file : str = "maze.txt"
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
                    line = (line.strip()).split("=")
                    if line[0] == "WIDTH":
                        self.width = int(line[1])
                    elif line[0] == "HEIGHT":
                        self.height = int(line[1])
                    elif line[0] == "ENTRY":
                        data = line[1].split(",")
                        self.entry = (int(data[0]), int(data[1]))
                    elif line[0] == "EXIT":
                        data = line[1].split(",")
                        self.exit = (int(data[0]), int(data[1]))
                    elif line[0] == "PERFECT":
                        self.perfect = True if line[1] == "True" else False
                    elif line[0] == "OUTPUT_FILE":
                        self.output_file = line[1]    
        except FileNotFoundError:
            print("ERROR: file not found")
            exit(1)
        except PermissionError:
            print("ERROR: file permissions")
            exit(1)
        except Exception as e:
            print(f"Unknoun ERROR: {e}")
            exit(1)

    def _validate_entry_exit(self) -> None:
        """Validate that entry and exit points are within bounds and not equal"""
        try:
            if not (0 <= self.entry[0] < self.height and 0 <= self.entry[1] < self.width):
                raise ValueError("Entry point out of bounds")
            if not (0 <= self.exit[0] < self.height and 0 <= self.exit[1] < self.width):
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
        if cel["N"]: val += 1
        if cel["E"]: val += 2
        if cel["S"]: val += 4
        if cel["W"]: val += 8
        return hex(val)[2:].upper()

    def save_to_file(self) -> None:
        """Write the current maze grid to the configured output file."""
        try:
            with open(self.hex_file, "w") as f:
                for y in range(self.height):
                    for x in range(self.width):
                        f.write(self._cell_to_hex((y, x)))
                    f.write("\n")
                f.write(f"ENTRY {self.entry[0]},{self.entry[1]}\n")
                f.write(f"EXIT {self.exit[0]},{self.exit[1]}\n")
        except Exception:
            print("save_to_file(): ERROR")

    def print_data(self) -> None: # delet me 
        """Print config data and dump the grid for debugging purposes."""
        print(f"WIDTH: {self.width}")
        print(f"HEIGHT: {self.height}")
        print(f"ENTRY: {self.entry}")
        print(f"EXIT: {self.exit}")
        print(f"OUTPUT_FILE: {self.output_file}")
        print(f"PERFECT: {self.perfect}")

        print("-------------------------------------")
        with open("2darr", "w") as f:
            f.write(json.dumps(self.grid, indent=2))
        print(json.dumps(self.grid, indent=2))

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

    def get_neighbors_cells(self, cell: Coord) -> list[Coord]:
        """ Get only neigbors of an cell that are not visited 
            return: 
                    list of cords (of neigbors)
        """
        neigbors: list[Coord] = []
        y, x = cell
        # check north
        if y -  1 >= 0 and self.grid[y -  1][x]["visited"] == False:
            neigbors.append((y - 1, x))
        # check east
        if x + 1 < self.width and self.grid[y][x + 1]["visited"] == False:
            neigbors.append((y, x + 1))
        # check south
        if y + 1 < self.height and self.grid[y + 1][x]["visited"] == False:
            neigbors.append((y + 1, x))
        # check west
        if x - 1 >= 0 and self.grid[y][x - 1]["visited"] == False:
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
        
    def _place_42_pattern(self) -> None:
        
        if self.width < 9 or self.height < 7:
            print("WARNING: maze too small to draw 42 pattern")
            return
 
       
        start_row = (self.height - 5) // 2
        start_col = (self.width - 7) // 2
 
        for (dr, dc) in PATTERN_42:
            y = start_row + dr
            x = start_col + dc
            self.grid[y][x]["visited"] = True

    def build_maze(self) -> None:
        """Generate the maze using iterative DFS with backtracking."""
        start = self.entry
        stack: list[Coord] = [start]
        y, x = start
        self.grid[y][x]["visited"] = True

        self._place_42_pattern()   # ← ADD THIS LINE

        while stack:
            neighbors = self.get_neighbors_cells(stack[-1])
            if neighbors:
                y1, x1 = neighbor = choice(neighbors)
                self.remove_walls(stack[-1], neighbor)
                self.grid[y1][x1]["visited"] = True
                stack.append(neighbor)
            else:
                stack.pop()
from typing import Tuple
import json

class Maze:
    env = "config.txt"
    def __init__(self) -> None:
        self.width: int = 3
        self.height: int = 3
        self.entry: Tuple[int, int]
        self.exit: Tuple[int, int]
        self.output_file : str = "maze.txt"
        self.perfect: bool
        self.grid: list[list[dict[str, bool]]] = []
        self._load_env_data()

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
        except PermissionError:
            print("ERROR: file permissions")
        except Exception as e:
            print(f"Unknoun ERROR: {e}")

    def print_data(self) -> None: # delet me 
        print(f"WIDTH: {self.width}")
        print(f"HEIGHT: {self.height}")
        print(f"ENTRY: {self.entry}")
        print(f"EXIT: {self.exit}")
        print(f"OUTPUT_FILE: {self.output_file}")
        print(f"PERFECT: {self.perfect}")

        print("-------------------------------------")
        print(json.dumps(self.grid, indent=2))

    def build_grid(self) -> None:
        """ Build grid using width and height """
        for j in range(self.height):
            lis: list[dict[str, bool]] = []
            for i in range(self.width):
                cell = {
                        "visited": False,
                        "N": True,
                        "E": True,
                        "S": True,
                        "W": True
                    }
                print((j, i))
                lis.append(cell)
            self.grid.append(lis)

    def get_neighbors_cells(self, cell: Tuple[int, int]) -> list[tuple[int, int]]:
        """ Get only neigbors of an cell that are not visited 
            return: 
                    list of cords (of neigbors)
        """
        neigbors: list[tuple[int, int]] = []
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

    def remove_walls(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> None:
        """ Remove walls bettwen two cells """
        y1, x1 = cell1
        y2, x2 = cell2
        # check North


def main() -> None:
    maze = Maze()
    maze.build_grid()
    maze.print_data()
    maze.grid[0][0]["visited"] = True
    print(".................")
    print(maze.get_neighbors_cells((1, 1)))
    print(".................")

    


if __name__ == "__main__":
    main()


from typing import Tuple, Any

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
        print(self.grid)

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


def main() -> None:
    maze = Maze()
    maze.build_grid()
    maze.print_data()
    maze.grid[0][0]["visited"] = True
    print(".................")
    print(maze.grid)
    


if __name__ == "__main__":
    main()


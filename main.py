from amazeing import Maze_


def main() -> None:
    """Create a maze, generate it, and save the result to file."""
    maze = Maze_()
    maze.build_grid()
    maze.print_data()
    print(".................")
    maze.build_maze()
    maze.save_to_file()


if __name__ == "__main__":
    main()


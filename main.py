from amazeing import Maze_


def main() -> None:
    """Create a maze, generate it, and save the result to file."""
    try:
        maze = Maze_()
        maze.build_grid()
        print(".................")
        maze.build_maze()
        maze.save_to_file()
        maze.print_data()
    except KeyboardInterrupt:
        print("\n\nYOU CLICKED CTRL + C\n")


if __name__ == "__main__":
    main()

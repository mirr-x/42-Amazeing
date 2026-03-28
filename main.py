from amazeing import Maze_


def main() -> None:
    """Create a maze, generate it, and save the result to file."""
    maze = Maze_()
    maze.build_grid()
    maze.print_data()
    print(".................")
    maze.build_maze()
    
    maze.drawer.draw_maze(maze.entry)
    maze.save_to_file()
    
    while True:
        print("\n=== A-Maze-ing ====")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            maze = Maze_()
            maze.build_grid()
            maze.build_maze()
            maze.drawer.draw_maze(maze.entry)
            maze.save_to_file()

        elif choice == "2":
            pass  # TODO: solve + show/hide path

        elif choice == "3":
            maze.drawer.rotate_color()
            maze.drawer.draw_maze(maze.entry)

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter 1-4.")


if __name__ == "__main__":
    main()


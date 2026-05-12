from mazegen import Maze_
import sys
import random


def main(config_path: str) -> None:
    """Create a maze, generate it, and save the result to file."""
    try:
        maze = Maze_(config_path)
        maze.build_grid()
        random.seed(maze.seed)
        maze.build_maze()

        maze.save_to_file()
        maze.drawer.draw_maze(maze.entry)
        if maze.width < 9 or maze.height < 7:
            print("\nWARNING: maze too small to draw 42 pattern")

        show_path = False
        bfs_path = None
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    while True:
        try:
            print("\n=== A-Maze-ing ====")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Animate path from entry to exit")
            print("5. Quit")
            choice = input("Choice (1-5): ").strip()

            if choice == "1":
                maze = Maze_(config_path)
                maze.build_grid()
                random.seed(maze.seed)
                maze.build_maze()
                show_path = False
                bfs_path = None
                maze.drawer.draw_maze(maze.entry)
                maze.save_to_file()
                if maze.width < 9 or maze.height < 7:
                    print("\nWARNING: maze too small to draw 42 pattern")

            elif choice == "2":
                show_path = not show_path
                if show_path:
                    bfs_path = maze.solve_bfs()

                    if bfs_path:
                        print(f"Shortest path found: {len(bfs_path)} steps.")

                    else:
                        print("No path found between entry and exit!")
                        show_path = False
                maze.drawer.draw_maze(
                    maze.entry, bfs_path if show_path else None)

            elif choice == "3":
                maze.drawer.rotate_color()
                maze.drawer.draw_maze(maze.entry)

            elif choice == "4":
                if not bfs_path:
                    bfs_path = maze.solve_bfs()
                if bfs_path:
                    maze.drawer.animate_path(bfs_path)
                    show_path = True
                else:
                    print("No path found between entry and exit!")

            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter 1-5.")
        except (Exception, KeyboardInterrupt):
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        raise SystemExit(1)
    main(sys.argv[1])

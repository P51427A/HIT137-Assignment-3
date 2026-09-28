import tkinter as tk

from puzzle_game import PuzzleGame


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 680


def main():
    """Create and run the image tile puzzle application."""
    root = tk.Tk()

    root.title("Image Tile Puzzle")
    root.geometry(
        str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT)
    )
    root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)

    application = PuzzleGame(root)
    application.pack(
        fill=tk.BOTH,
        expand=True
    )

    root.mainloop()


if __name__ == "__main__":
    main()
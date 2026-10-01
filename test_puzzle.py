from puzzle import Puzzle


IMAGE_PATH = "sample_images/shinchan.jpg"
GRID_SIZES = [3, 4, 5]


def test_grid_size(grid_size):
    """Test the main puzzle features for one grid size."""
    puzzle = Puzzle(grid_size)
    puzzle.load_image(IMAGE_PATH)

    tile_count = 0

    for position in range(grid_size * grid_size):
        tile = puzzle.get_tile_at_position(position)

        if tile is not None:
            tile_count += 1

    transformed_image = puzzle.get_transformed_image()

    print("\nGrid size:", grid_size, "x", grid_size)
    print("Image dimensions:", transformed_image.shape)
    print("Number of tiles:", tile_count)
    print("Initial moves:", puzzle.get_moves())
    print("Incorrect tiles:", puzzle.get_incorrect_count())
    print("Hints remaining:", puzzle.get_hints_remaining())

    puzzle.rotate_tile(0)
    puzzle.flip_tile(1)
    puzzle.swap_tiles(2, 3)

    print("Moves after three actions:", puzzle.get_moves())

    hint = puzzle.request_hint()

    print("Hint positions:", hint)
    print("Hints remaining after hint:", puzzle.get_hints_remaining())

    puzzle.solve()

    print("Moves after Solve:", puzzle.get_moves())
    print("Incorrect after Solve:", puzzle.get_incorrect_count())
    print("Puzzle complete:", puzzle.is_complete())


def main():
    """Test the puzzle at all required grid sizes."""
    for grid_size in GRID_SIZES:
        test_grid_size(grid_size)


if __name__ == "__main__":
    main()
    
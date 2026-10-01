import random

from image_processor import ImageProcessor
from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)


TRANSFORMATION_COUNTS = {
    3: 6,
    4: 12,
    5: 20
}

ROTATION_ANGLES = [90, 180, 270]
FLIP_DIRECTIONS = ["horizontal", "vertical"]
MAX_HINTS = 3


class Puzzle:
    """Manage the state and rules of one image puzzle."""

    def __init__(self, grid_size):
        """Create a puzzle using the selected grid size."""
        self.__grid_size = grid_size
        self.__processor = ImageProcessor(grid_size)
        self.__original_image = None
        self.__tiles = []
        self.__moves = 0
        self.__hints_used = 0
        self.__complete = False

    def load_image(self, file_path):
        """Load an image, create its tiles and scramble the puzzle."""
        image = self.__processor.load_image(file_path)

        self.__original_image = image.copy()
        self.__tiles = self.__processor.split_image(image)
        self.__moves = 0
        self.__hints_used = 0
        self.__complete = False

        self.__scramble()

    def __scramble(self):
        """Generate all random transformations and then apply them."""
        transformation_count = TRANSFORMATION_COUNTS[
            self.__grid_size
        ]

        available_tiles = self.__tiles.copy()
        random.shuffle(available_tiles)

        transformation_types = [
            "swap",
            "rotate",
            "flip"
        ]

        maximum_swaps = (
            len(self.__tiles) - transformation_count
        )

        while len(transformation_types) < transformation_count:
            allowed_types = ["rotate", "flip"]

            current_swaps = transformation_types.count("swap")

            if current_swaps < maximum_swaps:
                allowed_types.append("swap")

            selected_type = random.choice(allowed_types)
            transformation_types.append(selected_type)

        random.shuffle(transformation_types)

        transformations = []

        for transformation_type in transformation_types:
            if transformation_type == "swap":
                first_tile = available_tiles.pop()
                second_tile = available_tiles.pop()

                transformation = SwapTransformation(
                    first_tile,
                    second_tile
                )

            elif transformation_type == "rotate":
                tile = available_tiles.pop()
                angle = random.choice(ROTATION_ANGLES)

                transformation = RotateTransformation(
                    tile,
                    angle
                )

            else:
                tile = available_tiles.pop()
                direction = random.choice(FLIP_DIRECTIONS)

                transformation = FlipTransformation(
                    tile,
                    direction
                )

            transformations.append(transformation)

        for transformation in transformations:
            transformation.apply()

    def get_original_image(self):
        """Return the original prepared image."""
        return self.__original_image

    def get_transformed_image(self):
        """Return the current reassembled puzzle image."""
        if len(self.__tiles) == 0:
            return None

        return self.__processor.assemble_image(self.__tiles)

    def get_tile_at_position(self, position):
        """Return the tile currently occupying a grid position."""
        for tile in self.__tiles:
            if tile.get_current_position() == position:
                return tile

        return None

    def swap_tiles(self, first_position, second_position):
        """Swap two selected positions and count one move."""
        if self.__complete:
            return False

        if first_position == second_position:
            return False

        first_tile = self.get_tile_at_position(first_position)
        second_tile = self.get_tile_at_position(second_position)

        if first_tile is None or second_tile is None:
            return False

        transformation = SwapTransformation(
            first_tile,
            second_tile
        )
        transformation.apply()

        self.__moves += 1
        self.__check_completion()

        return True

    def rotate_tile(self, position):
        """Rotate one tile clockwise and count one move."""
        if self.__complete:
            return False

        tile = self.get_tile_at_position(position)

        if tile is None:
            return False

        transformation = RotateTransformation(tile, 90)
        transformation.apply()

        self.__moves += 1
        self.__check_completion()

        return True

    def flip_tile(self, position):
        """Flip one tile horizontally and count one move."""
        if self.__complete:
            return False

        tile = self.get_tile_at_position(position)

        if tile is None:
            return False

        transformation = FlipTransformation(
            tile,
            "horizontal"
        )
        transformation.apply()

        self.__moves += 1
        self.__check_completion()

        return True

    def get_incorrect_count(self):
        """Return the number of tiles that are not restored."""
        incorrect_count = 0

        for tile in self.__tiles:
            if not tile.is_correct():
                incorrect_count += 1

        return incorrect_count

    def __check_completion(self):
        """Update the puzzle's completion state."""
        if self.get_incorrect_count() == 0:
            self.__complete = True

    def request_hint(self):
        """Return an incorrect tile and its correct home position."""
        if self.__complete:
            return None

        if self.__hints_used >= MAX_HINTS:
            return None

        incorrect_tiles = []

        for tile in self.__tiles:
            if not tile.is_correct():
                incorrect_tiles.append(tile)

        if len(incorrect_tiles) == 0:
            return None

        selected_tile = random.choice(incorrect_tiles)
        self.__hints_used += 1

        return (
            selected_tile.get_current_position(),
            selected_tile.get_correct_position()
        )

    def solve(self):
        """Restore every tile and clear the move count."""
        for tile in self.__tiles:
            tile.reset()

        self.__moves = 0
        self.__complete = True

    def reshuffle(self):
        """Reset and scramble the currently loaded image again."""
        if len(self.__tiles) == 0:
            return False

        for tile in self.__tiles:
            tile.reset()

        self.__moves = 0
        self.__hints_used = 0
        self.__complete = False
        self.__scramble()

        return True

    def get_moves(self):
        """Return the number of player moves."""
        return self.__moves

    def get_hints_remaining(self):
        """Return the number of hints still available."""
        return MAX_HINTS - self.__hints_used

    def is_complete(self):
        """Return whether the puzzle has been completed."""
        return self.__complete

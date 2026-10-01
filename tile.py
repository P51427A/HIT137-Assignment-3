import cv2
import numpy as np


class Tile:
    """Represent one tile belonging to the image puzzle."""

    def __init__(self, image, position):
        """Create a tile with its image and correct grid position."""
        self.__original_image = image.copy()
        self.__current_image = image.copy()
        self.__correct_position = position
        self.__current_position = position

    def get_image(self):
        """Return the tile's currently displayed image."""
        return self.__current_image

    def get_correct_position(self):
        """Return the tile's correct position."""
        return self.__correct_position

    def get_current_position(self):
        """Return the tile's current position."""
        return self.__current_position

    def set_current_position(self, position):
        """Update the tile's current position."""
        self.__current_position = position

    def rotate(self, angle):
        """Rotate the tile clockwise by 90, 180 or 270 degrees."""
        if angle == 90:
            self.__current_image = cv2.rotate(
                self.__current_image,
                cv2.ROTATE_90_CLOCKWISE
            )
        elif angle == 180:
            self.__current_image = cv2.rotate(
                self.__current_image,
                cv2.ROTATE_180
            )
        elif angle == 270:
            self.__current_image = cv2.rotate(
                self.__current_image,
                cv2.ROTATE_90_COUNTERCLOCKWISE
            )

    def flip(self, direction):
        """Flip the tile horizontally or vertically."""
        if direction == "horizontal":
            self.__current_image = cv2.flip(
                self.__current_image,
                1
            )
        elif direction == "vertical":
            self.__current_image = cv2.flip(
                self.__current_image,
                0
            )

    def is_correct(self):
        """Return True when the tile has the correct position and orientation."""
        correct_position = (
            self.__current_position == self.__correct_position
        )

        correct_orientation = np.array_equal(
            self.__current_image,
            self.__original_image
        )

        return correct_position and correct_orientation

    def reset(self):
        """Restore the tile to its original position and orientation."""
        self.__current_image = self.__original_image.copy()
        self.__current_position = self.__correct_position
        
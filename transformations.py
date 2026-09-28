class Transformation:
    """Parent class for puzzle transformations."""

    def apply(self):
        """Apply a transformation to one or more tiles."""
        pass


class SwapTransformation(Transformation):
    """Swap the current positions of two tiles."""

    def __init__(self, first_tile, second_tile):
        """Store the two tiles that will be swapped."""
        self.__first_tile = first_tile
        self.__second_tile = second_tile

    def apply(self):
        """Exchange the current positions of the two tiles."""
        first_position = self.__first_tile.get_current_position()
        second_position = self.__second_tile.get_current_position()

        self.__first_tile.set_current_position(second_position)
        self.__second_tile.set_current_position(first_position)


class RotateTransformation(Transformation):
    """Rotate one tile by a specified angle."""

    def __init__(self, tile, angle):
        """Store the tile and its rotation angle."""
        self.__tile = tile
        self.__angle = angle

    def apply(self):
        """Rotate the selected tile."""
        self.__tile.rotate(self.__angle)


class FlipTransformation(Transformation):
    """Flip one tile in a specified direction."""

    def __init__(self, tile, direction):
        """Store the tile and its flip direction."""
        self.__tile = tile
        self.__direction = direction

    def apply(self):
        """Flip the selected tile."""
        self.__tile.flip(self.__direction)
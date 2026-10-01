import cv2

from tile import Tile


MAX_IMAGE_SIZE = 450
PADDING_COLOUR = (235, 235, 235)


class ImageProcessor:
    """Load, resize, divide and reassemble puzzle images."""

    def __init__(self, grid_size):
        """Create an image processor for the selected grid size."""
        self.__grid_size = grid_size

    def load_image(self, file_path):
        """Load and prepare an image for the puzzle."""
        image = cv2.imread(file_path)

        if image is None:
            raise ValueError("The selected file is not a valid image.")

        return self.__resize_and_pad(image)

    def __resize_and_pad(self, image):
        """Resize an image and pad it into an evenly divisible square."""
        height, width = image.shape[:2]

        target_size = MAX_IMAGE_SIZE - (
            MAX_IMAGE_SIZE % self.__grid_size
        )

        scale = min(
            target_size / width,
            target_size / height
        )

        new_width = int(width * scale)
        new_height = int(height * scale)

        if scale < 1:
            interpolation = cv2.INTER_AREA
        else:
            interpolation = cv2.INTER_LINEAR

        resized_image = cv2.resize(
            image,
            (new_width, new_height),
            interpolation=interpolation
        )

        horizontal_padding = target_size - new_width
        vertical_padding = target_size - new_height

        left_padding = horizontal_padding // 2
        right_padding = horizontal_padding - left_padding
        top_padding = vertical_padding // 2
        bottom_padding = vertical_padding - top_padding

        padded_image = cv2.copyMakeBorder(
            resized_image,
            top_padding,
            bottom_padding,
            left_padding,
            right_padding,
            cv2.BORDER_CONSTANT,
            value=PADDING_COLOUR
        )

        return padded_image

    def split_image(self, image):
        """Divide an image into Tile objects."""
        tiles = []

        height, width = image.shape[:2]
        tile_height = height // self.__grid_size
        tile_width = width // self.__grid_size

        for row in range(self.__grid_size):
            for column in range(self.__grid_size):
                start_y = row * tile_height
                end_y = start_y + tile_height
                start_x = column * tile_width
                end_x = start_x + tile_width

                tile_image = image[
                    start_y:end_y,
                    start_x:end_x
                ]

                position = row * self.__grid_size + column
                tile = Tile(tile_image, position)
                tiles.append(tile)

        return tiles

    def assemble_image(self, tiles):
        """Reassemble the tiles according to their current positions."""
        ordered_images = [None] * len(tiles)

        for tile in tiles:
            position = tile.get_current_position()
            ordered_images[position] = tile.get_image()

        rows = []

        for row_number in range(self.__grid_size):
            start = row_number * self.__grid_size
            end = start + self.__grid_size

            image_row = cv2.hconcat(
                ordered_images[start:end]
            )
            rows.append(image_row)

        complete_image = cv2.vconcat(rows)

        return complete_image

import cv2

from image_processor import ImageProcessor
from transformations import (
    SwapTransformation,
    RotateTransformation,
    FlipTransformation
)


def main():
    """Test image processing and tile transformations."""
    processor = ImageProcessor(3)

    original_image = processor.load_image(
        "sample_images/shinchan.jpg"
    )

    tiles = processor.split_image(original_image)

    transformations = [
        SwapTransformation(tiles[0], tiles[1]),
        RotateTransformation(tiles[2], 90),
        FlipTransformation(tiles[3], "horizontal")
    ]

    for transformation in transformations:
        transformation.apply()

    transformed_image = processor.assemble_image(tiles)

    incorrect_tiles = 0

    for tile in tiles:
        if not tile.is_correct():
            incorrect_tiles += 1

    print("Number of tiles:", len(tiles))
    print("Incorrect tiles:", incorrect_tiles)

    cv2.imshow("Original Image", original_image)
    cv2.imshow("Transformed Image", transformed_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    
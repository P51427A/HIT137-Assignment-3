# HIT137 Assignment 3 – Image Tile Puzzle

## Overview

This project is a desktop image puzzle developed for HIT137 Software Now. It demonstrates object-oriented programming, Tkinter GUI development and image processing with OpenCV.

The application loads an image, resizes and pads it, divides it into tiles and applies randomly generated swap, rotation and flip transformations. The player must restore the image using mouse controls.

## Group Members

| Name | Student ID |
|---|---|
| Pranjal Awasthi | S405821 |
| Rahul Neupane | S404801 |
| Milan Bhattarai | S403198 |
| Nischal Malla | S401733 |


## Features

- Supports JPG, JPEG, PNG and BMP images
- 3×3, 4×4 and 5×5 grid options
- Original and transformed images displayed side by side
- Random swap, rotation and flip transformations
- Transformation count increases with grid size
- No tile is targeted twice during initial scrambling
- Move and incorrect-tile counters
- Green ticks for correctly restored tiles
- Coloured border for the selected tile
- Maximum of three hints per image
- Solve button for instantly restoring the image
- Automatic completion detection and input locking
- Error handling for cancelled dialogs and invalid files

## Controls

| Action | Control |
|---|---|
| Select a tile | Left click |
| Deselect a tile | Left click the selected tile again |
| Swap tiles | Left click two different tiles |
| Rotate clockwise | Right click |
| Flip horizontally | Shift + left click |
| Display a hint | Hint button |
| Restore the puzzle | Solve button |

Each swap, rotation or flip counts as one move.

## Installation

Install the required Python packages:

`pip install -r requirements.txt`

## Running the Application

Run the program from the project directory:

`python main.py`

Choose the grid size before loading an image.

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Starts the Tkinter application |
| `puzzle_game.py` | Provides the GUI and mouse interactions |
| `puzzle.py` | Manages puzzle state, moves, hints and completion |
| `image_processor.py` | Loads, resizes, pads, divides and reassembles images |
| `tile.py` | Represents an individual puzzle tile |
| `transformations.py` | Contains swap, rotation and flip classes |
| `requirements.txt` | Lists the required packages |
| `github_link.txt` | Contains the public GitHub repository link |
| `test_component.py` | Tests image processing and transformations |
| `test_puzzle.py` | Tests puzzle logic at all three grid sizes |

## Object-Oriented Design

### Encapsulation

The `Tile` and `Puzzle` classes use private attributes and provide methods for controlled access and modification.

### Inheritance

`SwapTransformation`, `RotateTransformation` and `FlipTransformation` inherit from the parent `Transformation` class.

### Polymorphism

Each transformation class overrides the `apply()` method. Different transformation objects can therefore be stored together and processed using the same method call.

### Class Interaction

The GUI communicates with the `Puzzle` class, which uses `ImageProcessor`, `Tile` and the transformation classes to manage the game.

## Image Processing

OpenCV is used to:

- Load images from disk
- Resize images while preserving aspect ratio
- Pad images to create evenly divisible square grids
- Divide images using pixel-array slicing
- Rotate and flip tiles
- Reassemble tiles into one displayed image

The prepared image sizes are:

| Grid | Image size | Tile size |
|---|---:|---:|
| 3×3 | 450×450 | 150×150 |
| 4×4 | 448×448 | 112×112 |
| 5×5 | 450×450 | 90×90 |

## Testing Checklist

The application should be tested using:

- All three grid sizes
- JPG, PNG and BMP images
- Cancelled file selection
- Invalid and non-image files
- Tile selection and deselection
- Swapping, rotation and flipping
- Three-hint enforcement
- Solve functionality
- Manual puzzle completion
- Loading a new image after completing a round

## Repository

The public GitHub repository URL is provided in `github_link.txt`.
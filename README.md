# HIT137 Assignment 3 – Image Tile Puzzle Game

## Overview

This project is an image tile puzzle created for HIT137 Software Now using Python, Tkinter and OpenCV.

The program loads an image, resizes it and divides it into tiles. The tiles are then randomly swapped, rotated or flipped. The aim is to restore the original image using the mouse controls.

## Group Members

| Name | Student ID |
|---|---|
| Pranjal Awasthi | S405821 |
| Rahul Neupane | S404801 |
| Milan Bhattarai | S403198 |
| Nischal Malla | S401733 |

## Features

- Supports JPG, JPEG, PNG and BMP images
- Includes 3×3, 4×4 and 5×5 grid sizes
- Displays the original and puzzle images side by side
- Randomly swaps, rotates and flips tiles
- Uses more transformations for larger grids
- Prevents the same tile from being targeted twice during scrambling
- Counts the number of moves and incorrect tiles
- Shows a green tick on correctly restored tiles
- Provides up to three hints for each puzzle
- Includes Solve, Reshuffle and Clear Image buttons
- Detects when the puzzle has been completed
- Handles cancelled selections and invalid image files

## Controls

| Action | Control |
|---|---|
| Select a tile | Left click |
| Deselect a tile | Left click the selected tile again |
| Swap two tiles | Left click two different tiles |
| Rotate a tile clockwise | Right click |
| Flip a tile horizontally | Shift + left click |
| Show a hint | Hint button |
| Restore the full image | Solve button |
| Scramble the loaded image again | Reshuffle button |
| Remove the image from the program | Clear Image button |

A swap, rotation or flip counts as one move.

## Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Program

Run the following command from the project folder:

```bash
python main.py
```

Choose a grid size and then click **Load Image** to begin.

## Project Files

| File | Purpose |
|---|---|
| `main.py` | Starts the application |
| `puzzle_game.py` | Contains the Tkinter interface and mouse controls |
| `puzzle.py` | Manages the puzzle, moves, hints and completion |
| `image_processor.py` | Loads, resizes, pads and divides images |
| `tile.py` | Represents each image tile |
| `transformations.py` | Contains the swap, rotate and flip transformations |
| `requirements.txt` | Lists the required packages |
| `github_link.txt` | Contains the GitHub repository link |
| `test_component.py` | Tests the image-processing components |
| `test_puzzle.py` | Tests the puzzle using all three grid sizes |

## How It Works

The program uses separate classes for the interface, puzzle logic, image processing, tiles and transformations. The swap, rotate and flip classes share a parent transformation class and each has its own `apply()` method.

OpenCV prepares the selected image at upto 450×450 image while keeping its original aspect ratio. Padding is added when needed so the image can be divided evenly into 3×3, 4×4 or 5×5 tiles.

## Testing

The program was tested with all three grid sizes and with JPG, PNG and BMP images. The mouse controls, hints, counters, Solve, Reshuffle, Clear Image and puzzle-completion features were also tested.

## Repository

The public GitHub repository link is included in `github_link.txt`.
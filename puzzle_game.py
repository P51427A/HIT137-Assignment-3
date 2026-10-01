import cv2
import tkinter as tk

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from puzzle import Puzzle


CANVAS_SIZE = 450
GRID_COLOUR = "#777777"
SELECTION_COLOUR = "#c2410c"
HINT_COLOUR = "#0057b8"
CORRECT_COLOUR = "#00ff00"

BACKGROUND_COLOUR = "#edf2f7"
HEADER_COLOUR = "#17324d"
PANEL_COLOUR = "#ffffff"
TEXT_COLOUR = "#17212b"
SECONDARY_TEXT_COLOUR = "#425466"
LOAD_BUTTON_COLOUR = "#1f5f99"
HINT_BUTTON_COLOUR = "#a85d00"
SOLVE_BUTTON_COLOUR = "#176b3a"
RESHUFFLE_BUTTON_COLOUR = "#5c3d8f"
CLEAR_BUTTON_COLOUR = "#6b4f54"
DISABLED_BUTTON_COLOUR = "#9aa6b2"


class PuzzleGame(tk.Frame):
    """Provide the Tkinter interface for the image puzzle."""

    def __init__(self, master):
        """Create the puzzle application interface."""
        super().__init__(master, background=BACKGROUND_COLOUR)

        self.__puzzle = None
        self.__current_file_path = None
        self.__active_grid_size = 3
        self.__selected_position = None
        self.__hint_positions = None

        self.__original_photo = None
        self.__puzzle_photo = None

        self.__grid_variable = tk.IntVar(value=3)
        self.__moves_variable = tk.StringVar(value="Moves: -")
        self.__incorrect_variable = tk.StringVar(
            value="Tiles remaining: -"
        )
        self.__hints_variable = tk.StringVar(
            value="Hints remaining: -"
        )
        self.__message_variable = tk.StringVar(
            value="Choose a grid size and load an image to begin."
        )

        self.__create_widgets()
        self.__bind_events()
        self.__update_buttons()

    def __create_widgets(self):
        """Create and arrange all interface widgets."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        header_frame = tk.Frame(
            self,
            background=HEADER_COLOUR
        )
        header_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew"
        )
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(
            header_frame,
            text="HIT137 Image Tile Puzzle Game",
            font=("Arial", 20, "bold"),
            background=HEADER_COLOUR,
            foreground="white"
        )
        title_label.grid(
            row=0,
            column=0,
            pady=(5, 0)
        )

        subtitle_label = tk.Label(
            header_frame,
            text="Restore the image by swapping, rotating and flipping tiles",
            font=("Arial", 10),
            background=HEADER_COLOUR,
            foreground="#d9e7f3"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 5))

        message_label = tk.Label(
            header_frame,
            textvariable=self.__message_variable,
            font=("Arial", 9, "bold"),
            background=HEADER_COLOUR,
            foreground="#f4d06f",
            anchor="center",
            justify=tk.CENTER
        )
        message_label.grid(
            row=2,
            column=0,
            pady=(0, 5)
        )

        controls_frame = tk.Frame(
            self,
            background=PANEL_COLOUR,
            highlightthickness=1,
            highlightbackground="#c3ced8"
        )
        controls_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            pady=6,
            ipadx=12,
            ipady=5
        )

        grid_label = tk.Label(
            controls_frame,
            text="Grid size",
            font=("Arial", 10, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        )
        grid_label.pack(side=tk.LEFT, padx=5)

        self.__grid_menu = tk.OptionMenu(
            controls_frame,
            self.__grid_variable,
            3,
            4,
            5
        )
        self.__grid_menu.config(
            width=4,
            font=("Arial", 10, "bold"),
            background="#f4f7fa",
            activebackground="#e3ebf2",
            relief=tk.GROOVE
        )
        self.__grid_menu.pack(side=tk.LEFT, padx=5)

        load_button = tk.Button(
            controls_frame,
            text="Load Image",
            width=12,
            font=("Arial", 10, "bold"),
            background=LOAD_BUTTON_COLOUR,
            foreground="white",
            activebackground="#184b78",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.__load_image
        )
        load_button.pack(side=tk.LEFT, padx=(10, 5), ipady=2)

        self.__reshuffle_button = tk.Button(
            controls_frame,
            text="Reshuffle",
            width=11,
            font=("Arial", 10, "bold"),
            background=RESHUFFLE_BUTTON_COLOUR,
            foreground="white",
            activebackground="#472f70",
            activeforeground="white",
            disabledforeground="#eef2f5",
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.__reshuffle_puzzle
        )
        self.__reshuffle_button.pack(
            side=tk.LEFT,
            padx=5,
            ipady=2
        )

        self.__clear_button = tk.Button(
            controls_frame,
            text="Clear Image",
            width=11,
            font=("Arial", 10, "bold"),
            background=CLEAR_BUTTON_COLOUR,
            foreground="white",
            activebackground="#523c40",
            activeforeground="white",
            disabledforeground="#eef2f5",
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.__clear_image
        )
        self.__clear_button.pack(side=tk.LEFT, padx=5, ipady=2)

        divider = tk.Frame(
            controls_frame,
            background="#b7c4cf",
            width=2,
            height=30
        )
        divider.pack(side=tk.LEFT, padx=10)
        divider.pack_propagate(False)

        self.__hint_button = tk.Button(
            controls_frame,
            text="Hint",
            width=10,
            font=("Arial", 10, "bold"),
            background=HINT_BUTTON_COLOUR,
            foreground="white",
            activebackground="#824800",
            activeforeground="white",
            disabledforeground="#eef2f5",
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.__show_hint
        )
        self.__hint_button.pack(side=tk.LEFT, padx=5, ipady=2)

        self.__solve_button = tk.Button(
            controls_frame,
            text="Solve",
            width=10,
            font=("Arial", 10, "bold"),
            background=SOLVE_BUTTON_COLOUR,
            foreground="white",
            activebackground="#10522c",
            activeforeground="white",
            disabledforeground="#eef2f5",
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.__solve_puzzle
        )
        self.__solve_button.pack(side=tk.LEFT, padx=5, ipady=2)

        original_panel = tk.Frame(
            self,
            background=PANEL_COLOUR,
            highlightthickness=1,
            highlightbackground="#b7c4cf"
        )
        original_panel.grid(
            row=2,
            column=0,
            padx=(18, 9),
            pady=2
        )

        puzzle_panel = tk.Frame(
            self,
            background=PANEL_COLOUR,
            highlightthickness=1,
            highlightbackground="#b7c4cf"
        )
        puzzle_panel.grid(
            row=2,
            column=1,
            padx=(9, 18),
            pady=2
        )

        original_label = tk.Label(
            original_panel,
            text="Original Image",
            font=("Arial", 13, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        )
        original_label.pack(pady=(4, 3))

        puzzle_label = tk.Label(
            puzzle_panel,
            text="Puzzle Image",
            font=("Arial", 13, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        )
        puzzle_label.pack(pady=(4, 3))

        self.__original_canvas = tk.Canvas(
            original_panel,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            background="#e2e8ee",
            highlightthickness=2,
            highlightbackground="#667788"
        )
        self.__original_canvas.pack(padx=8, pady=(0, 6))

        self.__puzzle_canvas = tk.Canvas(
            puzzle_panel,
            width=CANVAS_SIZE,
            height=CANVAS_SIZE,
            background="#e2e8ee",
            highlightthickness=2,
            highlightbackground="#667788",
            cursor="hand2"
        )
        self.__puzzle_canvas.pack(padx=8, pady=(0, 6))

        status_frame = tk.Frame(
            self,
            background=PANEL_COLOUR,
            highlightthickness=1,
            highlightbackground="#c3ced8"
        )
        status_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=(6, 3),
            ipadx=8,
            ipady=3
        )

        tk.Label(
            status_frame,
            textvariable=self.__moves_variable,
            font=("Arial", 11, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            status_frame,
            textvariable=self.__incorrect_variable,
            font=("Arial", 11, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            status_frame,
            textvariable=self.__hints_variable,
            font=("Arial", 11, "bold"),
            background=PANEL_COLOUR,
            foreground=TEXT_COLOUR
        ).pack(side=tk.LEFT, padx=20)

        instruction_text = (
            "Left click: select or swap"
            "\t\tRight click: rotate clockwise\t\t"
            "Shift + left click: flip horizontally\n"
        )

        instruction_label = tk.Label(
            self,
            text=instruction_text,
            font=("Arial", 11),
            background=BACKGROUND_COLOUR,
            foreground="#283848",
            justify=tk.CENTER
        )
        instruction_label.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(1, 2)
        )

        footer_label = tk.Label(
            self,
            text="HIT137 Software Now  |  Assignment 3",
            font=("Arial", 10, "bold"),
            background=BACKGROUND_COLOUR,
            foreground=SECONDARY_TEXT_COLOUR
        )
        footer_label.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=(0, 4)
        )

    def __bind_events(self):
        """Connect mouse actions to the puzzle canvas."""
        self.__puzzle_canvas.bind(
            "<Button-1>",
            self.__handle_left_click
        )
        self.__puzzle_canvas.bind(
            "<Button-3>",
            self.__handle_right_click
        )
        self.__puzzle_canvas.bind(
            "<Shift-Button-1>",
            self.__handle_shift_left_click
        )

    def __load_image(self):
        """Ask the player to choose and load an image."""
        file_path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("Bitmap files", "*.bmp")
            ]
        )

        if file_path == "":
            return

        grid_size = self.__grid_variable.get()
        new_puzzle = Puzzle(grid_size)

        try:
            new_puzzle.load_image(file_path)
        except ValueError as error:
            messagebox.showerror(
                "Image Error",
                str(error)
            )
            return

        self.__puzzle = new_puzzle
        self.__current_file_path = file_path
        self.__active_grid_size = grid_size
        self.__selected_position = None
        self.__hint_positions = None
        self.__message_variable.set(
            "Puzzle loaded. Select a tile on the puzzle image."
        )

        self.__update_display()
        self.__update_status()
        self.__update_buttons()

    def __convert_to_photo(self, image):
        """Convert an OpenCV image into a Tkinter image."""
        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)

    def __update_display(self):
        """Redraw the original and transformed images."""
        if self.__puzzle is None:
            return

        original_image = self.__puzzle.get_original_image()
        transformed_image = self.__puzzle.get_transformed_image()

        self.__original_photo = self.__convert_to_photo(
            original_image
        )
        self.__puzzle_photo = self.__convert_to_photo(
            transformed_image
        )

        image_height, image_width = original_image.shape[:2]

        self.__original_canvas.config(
            width=image_width,
            height=image_height
        )
        self.__puzzle_canvas.config(
            width=image_width,
            height=image_height
        )

        self.__original_canvas.delete("all")
        self.__puzzle_canvas.delete("all")

        self.__original_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.__original_photo
        )

        self.__puzzle_canvas.create_image(
            0,
            0,
            anchor=tk.NW,
            image=self.__puzzle_photo
        )

        self.__draw_grid(image_width, image_height)
        self.__draw_correct_ticks(image_width, image_height)
        self.__draw_selection(image_width, image_height)
        self.__draw_hint(image_width, image_height)

    def __draw_grid(self, image_width, image_height):
        """Draw faint tile boundaries over the puzzle."""
        tile_width = image_width // self.__active_grid_size
        tile_height = image_height // self.__active_grid_size

        for number in range(1, self.__active_grid_size):
            x_position = number * tile_width
            y_position = number * tile_height

            self.__puzzle_canvas.create_line(
                x_position,
                0,
                x_position,
                image_height,
                fill=GRID_COLOUR
            )

            self.__puzzle_canvas.create_line(
                0,
                y_position,
                image_width,
                y_position,
                fill=GRID_COLOUR
            )

    def __draw_correct_ticks(self, image_width, image_height):
        """Draw a green tick on every correctly restored tile."""
        tile_width = image_width // self.__active_grid_size
        tile_height = image_height // self.__active_grid_size

        tile_total = (
            self.__active_grid_size *
            self.__active_grid_size
        )

        for position in range(tile_total):
            tile = self.__puzzle.get_tile_at_position(position)

            if tile is not None and tile.is_correct():
                column = position % self.__active_grid_size
                row = position // self.__active_grid_size

                right_x = (column + 1) * tile_width
                top_y = row * tile_height

                self.__puzzle_canvas.create_line(
                    right_x - 22,
                    top_y + 13,
                    right_x - 16,
                    top_y + 19,
                    right_x - 7,
                    top_y + 7,
                    fill=CORRECT_COLOUR,
                    width=5
                )

    def __draw_selection(self, image_width, image_height):
        """Draw a coloured border around the selected tile."""
        if self.__selected_position is None:
            return

        tile_width = image_width // self.__active_grid_size
        tile_height = image_height // self.__active_grid_size

        column = (
            self.__selected_position %
            self.__active_grid_size
        )
        row = (
            self.__selected_position //
            self.__active_grid_size
        )

        start_x = column * tile_width
        start_y = row * tile_height
        end_x = start_x + tile_width
        end_y = start_y + tile_height

        self.__puzzle_canvas.create_rectangle(
            start_x + 2,
            start_y + 2,
            end_x - 2,
            end_y - 2,
            outline=SELECTION_COLOUR,
            width=4
        )

    def __draw_hint(self, image_width, image_height):
        """Draw hint circles on the puzzle and original image."""
        if self.__hint_positions is None:
            return

        current_position, correct_position = (
            self.__hint_positions
        )

        self.__draw_circle(
            self.__puzzle_canvas,
            current_position,
            image_width,
            image_height
        )

        self.__draw_circle(
            self.__original_canvas,
            correct_position,
            image_width,
            image_height
        )

    def __draw_circle(
        self,
        canvas,
        position,
        image_width,
        image_height
    ):
        """Draw a blue hint circle at a grid position."""
        tile_width = image_width // self.__active_grid_size
        tile_height = image_height // self.__active_grid_size

        column = position % self.__active_grid_size
        row = position // self.__active_grid_size

        centre_x = column * tile_width + tile_width // 2
        centre_y = row * tile_height + tile_height // 2

        radius = min(tile_width, tile_height) // 6

        canvas.create_oval(
            centre_x - radius,
            centre_y - radius,
            centre_x + radius,
            centre_y + radius,
            outline=HINT_COLOUR,
            width=4
        )

    def __get_clicked_position(self, event):
        """Convert mouse coordinates into a grid position."""
        if self.__puzzle is None:
            return None

        image = self.__puzzle.get_transformed_image()
        image_height, image_width = image.shape[:2]

        if (
            event.x < 0 or
            event.y < 0 or
            event.x >= image_width or
            event.y >= image_height
        ):
            return None

        tile_width = image_width // self.__active_grid_size
        tile_height = image_height // self.__active_grid_size

        column = event.x // tile_width
        row = event.y // tile_height

        if (
            column >= self.__active_grid_size or
            row >= self.__active_grid_size
        ):
            return None

        return row * self.__active_grid_size + column

    def __handle_left_click(self, event):
        """Select, deselect or swap puzzle tiles."""
        if event.state & 0x0001:
            return "break"

        if (
            self.__puzzle is None or
            self.__puzzle.is_complete()
        ):
            return "break"

        position = self.__get_clicked_position(event)

        if position is None:
            return "break"

        if self.__selected_position is None:
            self.__selected_position = position
            row = position // self.__active_grid_size + 1
            column = position % self.__active_grid_size + 1
            self.__message_variable.set(
                "Selected tile: row " + str(row) +
                ", column " + str(column) + "."
            )

        elif self.__selected_position == position:
            self.__selected_position = None
            self.__message_variable.set(
                "Tile deselected. Select another tile."
            )

        else:
            move_made = self.__puzzle.swap_tiles(
                self.__selected_position,
                position
            )

            self.__selected_position = None

            if move_made:
                self.__hint_positions = None
                self.__message_variable.set(
                    "Tiles swapped. Select a tile for the next move."
                )
                self.__after_move()

                return "break"

        self.__update_display()
        return "break"

    def __handle_right_click(self, event):
        """Rotate the clicked tile clockwise."""
        if (
            self.__puzzle is None or
            self.__puzzle.is_complete()
        ):
            return "break"

        position = self.__get_clicked_position(event)

        if position is not None:
            move_made = self.__puzzle.rotate_tile(position)

            if move_made:
                self.__selected_position = None
                self.__hint_positions = None
                self.__message_variable.set(
                    "Tile rotated clockwise."
                )
                self.__after_move()

        return "break"

    def __handle_shift_left_click(self, event):
        """Flip the clicked tile horizontally."""
        if (
            self.__puzzle is None or
            self.__puzzle.is_complete()
        ):
            return "break"

        position = self.__get_clicked_position(event)

        if position is not None:
            move_made = self.__puzzle.flip_tile(position)

            if move_made:
                self.__selected_position = None
                self.__hint_positions = None
                self.__message_variable.set(
                    "Tile flipped horizontally."
                )
                self.__after_move()

        return "break"

    def __after_move(self):
        """Update the game after a valid player move."""
        self.__update_display()
        self.__update_status()
        self.__update_buttons()

        if self.__puzzle.is_complete():
            self.__message_variable.set(
                "Puzzle complete. All tiles are in the correct position."
            )
            messagebox.showinfo(
                "Puzzle Complete",
                "Congratulations! You restored the image."
            )

    def __show_hint(self):
        """Request and display one puzzle hint."""
        if self.__puzzle is None:
            return

        self.__hint_positions = self.__puzzle.request_hint()

        if self.__hint_positions is not None:
            current_position, correct_position = self.__hint_positions
            current_row = current_position // self.__active_grid_size + 1
            current_column = current_position % self.__active_grid_size + 1
            correct_row = correct_position // self.__active_grid_size + 1
            correct_column = correct_position % self.__active_grid_size + 1
            self.__message_variable.set(
                "Hint: puzzle tile at row " + str(current_row) +
                ", column " + str(current_column) +
                " belongs at row " + str(correct_row) +
                ", column " + str(correct_column) + "."
            )

        self.__update_display()
        self.__update_status()
        self.__update_buttons()

    def __solve_puzzle(self):
        """Instantly restore the complete puzzle."""
        if self.__puzzle is None:
            return

        self.__puzzle.solve()
        self.__selected_position = None
        self.__hint_positions = None
        self.__message_variable.set(
            "Puzzle solved. Load another image to play again."
        )

        self.__update_display()
        self.__update_status()
        self.__update_buttons()

        messagebox.showinfo(
            "Puzzle Solved",
            "The puzzle has been restored."
        )

    def __reshuffle_puzzle(self):
        """Scramble the loaded image again and reset the round."""
        if self.__puzzle is None:
            return

        grid_size = self.__grid_variable.get()

        if grid_size != self.__active_grid_size:
            new_puzzle = Puzzle(grid_size)

            try:
                new_puzzle.load_image(self.__current_file_path)
            except ValueError as error:
                messagebox.showerror(
                    "Image Error",
                    str(error)
                )
                return

            self.__puzzle = new_puzzle
            self.__active_grid_size = grid_size
        else:
            if not self.__puzzle.reshuffle():
                return

        self.__selected_position = None
        self.__hint_positions = None
        self.__message_variable.set(
            "Image reshuffled as a " + str(grid_size) +
            " x " + str(grid_size) +
            " grid. Moves and hints have been reset."
        )

        self.__update_display()
        self.__update_status()
        self.__update_buttons()

    def __clear_image(self):
        """Clear the loaded image and return to the initial state."""
        self.__puzzle = None
        self.__current_file_path = None
        self.__selected_position = None
        self.__hint_positions = None
        self.__original_photo = None
        self.__puzzle_photo = None

        self.__original_canvas.delete("all")
        self.__puzzle_canvas.delete("all")

        self.__moves_variable.set("Moves: -")
        self.__incorrect_variable.set("Tiles remaining: -")
        self.__hints_variable.set("Hints remaining: -")
        self.__message_variable.set(
            "Choose a grid size and load an image to begin."
        )

        self.__update_buttons()

    def __update_status(self):
        """Update moves, incorrect tiles and hints."""
        if self.__puzzle is None:
            return

        self.__moves_variable.set(
            "Moves: " + str(self.__puzzle.get_moves())
        )

        self.__incorrect_variable.set(
            "Tiles remaining: " +
            str(self.__puzzle.get_incorrect_count())
        )

        self.__hints_variable.set(
            "Hints remaining: " +
            str(self.__puzzle.get_hints_remaining())
        )

    def __update_buttons(self):
        """Enable or disable the puzzle buttons appropriately."""
        if self.__puzzle is None:
            self.__hint_button.config(state=tk.DISABLED)
            self.__solve_button.config(state=tk.DISABLED)
            self.__reshuffle_button.config(state=tk.DISABLED)
            self.__clear_button.config(state=tk.DISABLED)
            self.__hint_button.config(background=DISABLED_BUTTON_COLOUR)
            self.__solve_button.config(background=DISABLED_BUTTON_COLOUR)
            self.__reshuffle_button.config(
                background=DISABLED_BUTTON_COLOUR
            )
            self.__clear_button.config(
                background=DISABLED_BUTTON_COLOUR
            )
            return

        self.__reshuffle_button.config(
            state=tk.NORMAL,
            background=RESHUFFLE_BUTTON_COLOUR
        )
        self.__clear_button.config(
            state=tk.NORMAL,
            background=CLEAR_BUTTON_COLOUR
        )

        if self.__puzzle.is_complete():
            self.__hint_button.config(
                state=tk.DISABLED,
                background=DISABLED_BUTTON_COLOUR
            )
            self.__solve_button.config(
                state=tk.DISABLED,
                background=DISABLED_BUTTON_COLOUR
            )
            return

        self.__solve_button.config(state=tk.NORMAL)
        self.__solve_button.config(background=SOLVE_BUTTON_COLOUR)

        if self.__puzzle.get_hints_remaining() > 0:
            self.__hint_button.config(state=tk.NORMAL)
            self.__hint_button.config(background=HINT_BUTTON_COLOUR)
        else:
            self.__hint_button.config(state=tk.DISABLED)
            self.__hint_button.config(background=DISABLED_BUTTON_COLOUR)

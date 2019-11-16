# By: Joe Armitage
# Institution: UTSC

import xwordAPI as xword
from tkinter import ttk, simpledialog, messagebox, Tk, Frame, Label


def word_fits(word, row, column, direction):
    '''(str, int, int, str) -> NoneType'''
    if column >= xword.width or row >= xword.height:
        return False
    if direction == "H":
        if xword.fit_word_horizontal(row, column, word):
            return True
    elif direction == "V":
        if xword.fit_word_vertical(row, column, word):
            return True


def place_word(word, row, column, direction):
    if word_fits(word, row, column, direction):
        xword.put_word(word, row, column, direction)


class CrosswordProgram():
    def __init__(self):
        """(NoneType) -> NoneType
        Creates a window representing the crossword puzzle
        """
        self.new_width = xword.width
        self.new_height = xword.height

        # Creates the main window
        self.wn = Tk()
        self.wn.title("My Crossword Puzzle")
        self.build_puzzle()
        self.build_commands()

    def build_commands(self):
        # Create a frame for the command buttons
        cmd_frame = ttk.Labelframe(self.wn, text="Commands")
        cmd_frame.grid(row=0, column=2, padx=15)
        # Create the command buttons
        reset_button = ttk.Button(cmd_frame, text="Rebuild",
                                  command=self.rebuilder)
        reset_button.grid(row=1, column=0)
        row_num_scale_label = ttk.Label(cmd_frame, text="Number of Rows:")
        row_num_scale_label.grid(row=2, column=0, pady=5)
        row_num_scale = ttk.Scale(cmd_frame, command=self.set_new_height,
                                  from_=4, to=21, value=9)
        row_num_scale.grid(row=3, column=0)
        col_num_scale_label = ttk.Label(cmd_frame, text="Number of Columns:")
        col_num_scale_label.grid(row=4, column=0, pady=5)
        col_num_scale = ttk.Scale(cmd_frame, command=self.set_new_width,
                                  from_=3, to=51, value=15)
        col_num_scale.grid(row=5, column=0, pady=5)
        default_button = ttk.Button(cmd_frame, text="OG Puzzle",
                                    command=self.original_puzzle)
        default_button.grid(row=6, column=0)

    def build_puzzle(self):
        """ Create the puzzle as a grid of Label objects"""
        # Create a frame for the puzzle
        self.pz_frame = Frame(self.wn)
        self.pz_frame.grid(row=0, column=0)
        # Create a frame for the letter boxes
        self.letters_frame = Frame(self.pz_frame)
        self.letters_frame.grid(row=0, column=1)
        # Create a frame for the row number labels
        self.row_num_frame = Frame(self.pz_frame)
        self.row_num_frame.grid(row=0, column=0)
        # Create a frame for the column number labels
        self.col_num_frame = Frame(self.pz_frame)
        self.col_num_frame.grid(row=1, column=1)

        self.puzzle_labels = []
        row_num = 0
        for row in xword.puzzle:
            char_num = 0
            row_of_labels = []
            # Create the column of row number labels
            row_label = Label(self.row_num_frame, text=str(row_num),
                              height=2, width=2)
            row_label.grid(row=row_num+1, column=char_num)
            for char in row:
                if row_num < 1:
                    # Create the row of column number labels
                    column_label = Label(self.col_num_frame,
                                         text=str(char_num),
                                         height=1, width=3)
                    column_label.grid(row=row_num, column=char_num)
                # Create the grid of letters and words
                letter_box = Label(self.letters_frame, text=char,
                                   relief="sunken", height=2, width=3)
                if xword.is_empty(char):
                    letter_box["bg"] = "black"
                letter_box.grid(row=row_num, column=char_num)
                letter_box.bind("<ButtonPress-1>", self.add_word)
                row_of_labels.append(letter_box)
                char_num += 1
            self.puzzle_labels.append(row_of_labels)
            row_num += 1

    def add_word(self, event):
        # Identify the column and row of the label clicked
        starting_box = event.widget
        row_idx = 0
        for row in self.puzzle_labels:
            col_idx = 0
            for col in row:
                if starting_box is self.puzzle_labels[row_idx][col_idx]:
                    start_col = col_idx
                    start_row = row_idx
                col_idx += 1
            row_idx += 1

        # Spawn a dialog box demanding the word to be input
        new_word = None
        direction = None
        attempt = 0
        while attempt == 0 or (direction in ("H", "V") and new_word and
                               not word_fits(new_word, start_row,
                                             start_col, direction)):
            if attempt > 0:
                messagebox.showerror("Error", "That doesn't fit")
            new_word = simpledialog.askstring(
                "Input", "What word would you like to add?", parent=self.wn)
            if new_word is not None:
                new_word = new_word.upper()
                horizontal = messagebox.askyesnocancel(
                    "Direction",
                    """Do you want this added Horizonally?
If No, it will be added Vertically""",
                    parent=self.wn)
                if horizontal:
                    direction = "H"
                elif horizontal is False:
                    direction = "V"
            attempt += 1
        if new_word and direction:
            place_word(new_word, start_row, start_col, direction)
            self.pz_frame.destroy()
            self.build_puzzle()

    def rebuilder(self):
        xword.width = int(float(self.new_width))
        xword.height = int(float(self.new_height))
        xword.puzzle = [" "*xword.width for x in range(xword.height)]
        self.pz_frame.destroy()
        self.build_puzzle()

    def original_puzzle(self):
        xword.width = int(float(self.new_width))
        xword.height = int(float(self.new_height))
        xword.puzzle = [" "*xword.width for x in range(xword.height)]
        default_puzzle()
        self.pz_frame.destroy()
        self.build_puzzle()

    def set_new_width(self, new_width):
        self.new_width = new_width

    def set_new_height(self, new_height):
        self.new_height = new_height


def default_puzzle():
    # Play with these all you like to make your own puzzle
    place_word("PYTHON", 0, 0, "H")
    place_word("TESTING", 0, 2, "V")
    place_word("STRING", 2, 2, "H")
    place_word("INTEGER", 2, 5, "V")
    place_word("NIGHT", 4, 1, "H")
    place_word("GO", 2, 7, "V")
    place_word("OVERTIME", 3, 7, "H")
    place_word("WEIRD", 0, 10, "V")
    place_word("DUDE", 0, 14, "V")
    place_word("GINGER", 6, 2, "H")
    place_word("WHAT", 5, 12, "V")
    place_word("THE", 6, 11, "H")
    place_word("WOW", 7, 8, "H")
    place_word("Y", 5, 9, "V")


if __name__ == "__main__":
    xword.width = 15
    xword.height = 9
    xword.puzzle = [" "*xword.width for x in range(xword.height)]

    default_puzzle()

    # Create the Crossword Program
    active_program = CrosswordProgram()
    # Display the GUI window and wait for input
    active_program.wn.mainloop()

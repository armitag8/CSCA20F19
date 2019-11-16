# Implementation: Joe Armitage
# Design: Ilir Dema
# Institution: UTSC


def is_empty(c):
    '''(str) -> bool

    Tests the character c for similarity to the empty string or space
    character string.

    REQ:
    c: a single character

    Examples:
    >>> is_empty("")
    True

    >>> is_empty(" ")
    True

    >>> is_empty("a")
    False

    >>> is_empty("1")
    False

    >>> is_empty(".")
    False
    '''
    return (("" == c) or (" " == c))


def char_left(row, col):
    ''' (int, int) -> str

        row: row number, an integer from 0 to height-1
        col: column number, an integer from 0 to width-1
        returns: the puzzle character to the left of (row, col)
                 or "" if col == 0

        >>> char_left(0, 0)
        ''

        >>> char_left(0, 1)
        'p'
    '''
    if col > 0:
        character = puzzle[row][col-1]
    else:
        character = ""
    return character


def char_right(row, col):
    ''' (int, int) -> str

        row: row number, an integer from 0 to height-1
        col: column number, an integer from 0 to width-1
        returns: the puzzle character to the right of (row, col)
                 or "" if col == width-1

        >>> char_right(0, width-1)
        ''

        >>> char_right(0, 0)
        'y'
        '''
    if col < width-1:
        character = puzzle[row][col+1]
    else:
        character = ""
    return character


def char_above(row, col):
    ''' (int, int) -> str

        row: row number, an integer from 0 to height-1
        col: column number, an integer from 0 to width-1
        returns: the puzzle character above (row, col)
                 or "" if row == 0

        >>> char_above(0, width)
        ''

        >>> char_above(1, 0)
        'p'

        >>> char_above(1,1)
        'y'
        '''
    if row > 0:
        character = puzzle[row-1][col]
    else:
        character = ""
    return character


def char_below(row, col):
    ''' (int, int) -> str

        row: row number, an integer from 0 to height-1
        col: column number, an integer from 0 to width-1
        returns: the puzzle character below (row, col)
                 or "" if row == height-1

        >>> char_below(0, 0)
        ' '

        >>> char_below(0, 2)
        'e'

        >>> char_below(height-1, 1)
        ''
    '''
    if row < height-1:
        character = puzzle[row+1][col]
    else:
        character = ""
    return character


def fit_char_horizontal(row, col, c):
    ''' (int, int, str) -> bool

        row: row number, from 0 to height-1
        col: column number, from 0 to width-1
        c: a character
        returns: True, if c fits into puzzle horizontally
                 Otherwise False.

        >>> fit_char_horizontal(2, 2, "s")
        True

        >>> fit_char_horizontal(2, 2, "t")
        False

        >>> fit_char_horizontal(2, 3, "t")
        True

        >>> fit_char_horizontal(2, 0, "z")
        True
    '''
    # Assign the default return value to False
    can_fit = False

    # If the character already exists at the given coordinates, it fits
    if c == puzzle[row][col]:
        can_fit = True

    # Else, if the character at given coordinates is empty, check neighbours
    elif is_empty(puzzle[row][col]):
        # If neighbouring characters are empty, it fits
        if is_empty(char_above(row, col)) and is_empty(char_below(row, col)):
            can_fit = True

    return can_fit


def fit_char_vertical(row, col, c):
    ''' (int, int, str) -> bool

        row: row number, from 0 to height-1
        col: column number, from 0 to width-1
        c: a character
        returns: True, if c fits into puzzle vertically
                 Otherwise False.

        >>> fit_char_vertical(1, 6, "i")
        True

        >>> fit_char_vertical(2, 6, "t")
        False

        >>> fit_char_vertical(2, 6, "n")
        True

        >>> fit_char_vertical(2, 0, "z")
        True
    '''
    # Assign the default return value to False
    can_fit = False

    # If the character already exists at the given coordinates, it fits
    if c == puzzle[row][col]:
        can_fit = True

    # Else, if the character at given coordinates is empty, check neighbours
    elif is_empty(puzzle[row][col]):
        # If neighbouring characters are empty, it fits
        if is_empty(char_right(row, col)) and is_empty(char_left(row, col)):
            can_fit = True

    return can_fit


def fit_word_horizontal(row, col, word):
    ''' (int, int, str) -> bool
        row: row number, from 0 to height-1
        col: column number, from 0 to width-1
        returns: True if word fits in the puzzle horizontally,
        starting from the position (row, col)
    '''
    lenw = len(word)
    if not is_empty(char_left(row, col)):
        return False
    if not is_empty(char_right(row, col+lenw-1)):
        return False
    for c in word:
        if col > width-1:
            return False
        if not fit_char_horizontal(row, col, c):
            return False
        col = col + 1
    return True


def fit_word_vertical(row, col, word):
    ''' (int, int, str) -> bool
        row: row number, from 0 to height-1
        col: column number, from 0 to width-1
        returns: True if word fits in the puzzle vertically,
        starting from the position (row, col)
    '''
    lenw = len(word)
    if not is_empty(char_above(row, col)):
        return False
    if not is_empty(char_below(row+lenw-1, col)):
        return False
    for c in word:
        if row > height-1:
            return False
        if not fit_char_vertical(row, col, c):
            return False
        row = row + 1
    return True


def put_word(word, row, col, direction):
    ''' (str, int, int, str) -> NoneType
        Adds word to the puzzle starting from (row, col) in
        the given direction
    '''
    for c in word:
        # Replace the character at row, column with c
        puzzle[row] = puzzle[row][0:col] + c + puzzle[row][col+1:width]
        if direction == "H":
            # Set the variable col to the value of the next available column
            col = next_col(col)
        else:
            # Set the variable row to the value of the next available row
            row = next_row(row)


def next_col(x):
    ''' (int) -> int
        returns next column to the column x
    '''
    if x < width-1:
        x = x + 1
    return x


def next_row(y):
    ''' (int) -> int
        returns next row to the row y
    '''
    if y < height-1:
        y = y + 1
    return y


def draw_puzzle():
    ''' () -> str
    '''
    result = ''
    for row in range(height):
        result = result + puzzle[row] + "\n"
    return result


puzzle = ['python    ', '  e   i   ', '  string  ', '  t   t   ']
width = 10
height = 4

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

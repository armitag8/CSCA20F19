# By: Ilir Dema
# Institution: UTSC


import unittest

try:
    import xwordAPI as xword
except Exception:
    print("Cannot find xword.py, is it in the same folder?")
    exit(1)

xword.width = 14
xword.height = 7
xword.puzzle = ['     t        ',
                '     e        ',
                '    assignment',
                '     t        ',
                '     i        ',
                'python        ',
                '     g        ']
xword.puzzle_copy = xword.puzzle[:]


class AssignmentTests(unittest.TestCase):

    # tests for task 1

    def test_is_empty_on_empty_string(self):
        self.assertTrue(xword.is_empty(""), "Should return true")

    def test_is_empty_on_empty_string2(self):
        self.assertTrue(xword.is_empty(' '),
                        "Should also be considered an empty string")

    def test_is_empty_non_empty_string(self):
        result = xword.is_empty(' string')
        result = result or not isinstance(result, bool)
        self.assertFalse(result, 'should be false')

    def test_is_empty_non_empty_string1(self):
        result = xword.is_empty('a')
        result = result or not isinstance(result, bool)
        self.assertFalse(result, 'should be false')

    # tests for task 2

    def test_char_left_on_origin(self):
        self.assertTrue(xword.is_empty(xword.char_left(0, 0)),
                        'should be the empty string')

    def test_char_left(self):
        self.assertEqual(xword.char_left(2, 5), 'a')

    def test_char_left_empty_block(self):
        self.assertEqual(xword.char_left(0, 7), ' ')

    def test_char_left_on_firstcol(self):
        self.assertTrue(xword.is_empty(xword.char_left(3, 0)),
                        'should be the empty string')

    # tests for task3

    def test_char_right_on_end_of_puzzle(self):
        self.assertTrue(xword.is_empty(
            xword.char_right(6, 13)), 'should be empty')

    def test_char_right(self):
        self.assertEqual(xword.char_right(0, 4), 't')

    def test_char_right_empty_block(self):
        self.assertTrue(xword.is_empty(xword.char_right(2, 2)),
                        'should be an empty square')

    # tests for task4

    def test_char_above_on_origin(self):
        self.assertTrue(xword.is_empty(
            xword.char_above(0, 0)), 'should be empty')

    def test_char_above(self):
        self.assertEqual(xword.char_above(2, 5), 'e')

    def test_above_empty_block(self):
        self.assertEqual(xword.char_above(2, 4), ' ')

    # tests for task 5

    def test_char_below_outside_of_puzzle(self):
        self.assertTrue(xword.is_empty(
            xword.char_below(0, 13)), 'should be empty')

    def test_char_below(self):
        self.assertEqual(xword.char_below(1, 5), 's')

    def test_char_below_empty_block(self):
        self.assertEqual(xword.char_below(0, 13), ' ')

    # tests for task 6

    def test_fit_char_horizontal_char_already_there(self):
        self.assertTrue(xword.fit_char_horizontal(0, 5, 't'),
                        'this letter is already in the puzzle at that location')

    def test_fit_char_horizontal_char_below(self):
        result = xword.fit_char_horizontal(1, 6, 's')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'cant fit in this character here, s below it')

    def test_fit_char_horizontal_char_above(self):
        result = xword.fit_char_horizontal(3, 6, 's')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'cant fit in this character here, s above it')

    def test_fit_char_horizontal_works(self):
        self.assertTrue(xword.fit_char_horizontal(6, 6, 'r'),
                        "should be able to fit in the puzzle")

    def test_fit_char_horizontal_space_taken(self):
        result = xword.fit_char_horizontal(6, 5, 'e')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'there is already a different letter at that location')

    # tests for task 7

    def test_fit_char_vertical_char_already_there(self):
        self.assertTrue(xword.fit_char_vertical(1, 5, 'e'),
                        'this character is already in that location')

    def test_fit_char_vertical_space_taken(self):
        result = xword.fit_char_vertical(1, 5, 's')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'there is already a character in that location')

    def test_fit_char_vertical_char_left(self):
        result = xword.fit_char_vertical(3, 6, 'i')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'cannot fit a character there, there is a char to the left of it')

    def test_fit_char_vertical_char_right(self):
        result = xword.fit_char_vertical(3, 4, 'i')
        result = result or not isinstance(result, bool)
        self.assertFalse(result,
                         'cannot fit a character there, there is already a character'
                         'to the right of it')

    def test_fit_char_vertical_works(self):
        self.assertTrue(xword.fit_char_vertical(3, 9, 'o'),
                        "should be able to put a character there")

    # tests for task 8, 9, 10

    def test_put_word_horizontally(self):
        if xword.fit_word_horizontal(6, 5, 'get'):
            xword.put_word('get', 6, 5, 'H')
        new_puzzle = ['     t        ',
                      '     e        ',
                      '    assignment',
                      '     t        ',
                      '     i        ',
                      'python        ',
                      '     get      ']
        self.assertEqual(xword.puzzle, new_puzzle, 'get should fit in 6, 5')
        xword.puzzle = xword.puzzle_copy[:]

    def try_put_word_horizontally_doesnt_fit_grid(self):
        new_puzzle = xword.puzzle[:]
        if xword.fit_word_horizontal(4, 5, 'integration'):
            xword.put_word('integration', 4, 5, 'H')
        self.assertEqual(xword.puzzle, new_puzzle,
                         'integration does not fit so puzzle should not change')
        xword.puzzle = xword.puzzle_copy[:]  # just in case

    def try_put_word_horizontally_another_word_there(self):
        new_puzzle = xword.puzzle[:]
        if xword.fit_word_horizontal(5, 0, 'krypton'):
            xword.put_word('krypton', 5, 0, 'H')
        self.assertEqual(xword.puzzle, new_puzzle,
                         'the word python is already in that location')
        xword.puzzle = xword.puzzle_copy[:]  # just in case

    def test_put_word_vertically(self):
        if xword.fit_word_vertical(2, 9, 'no'):
            xword.put_word('no', 2, 9, 'V')
        new_puzzle = ['     t        ',
                      '     e        ',
                      '    assignment',
                      '     t   o    ',
                      '     i        ',
                      'python        ',
                      '     g        ']
        self.assertEqual(xword.puzzle, new_puzzle, 'no should fit in 2, 9')
        xword.puzzle = xword.puzzle_copy[:]

    def test_fit_word_vertically_doesnt_fit_grid(self):
        new_puzzle = xword.puzzle[:]
        if xword.fit_word_vertical(5, 0, 'program'):
            xword.put_word('program', 5, 0, 'V')
        self.assertEqual(xword.puzzle, new_puzzle,
                         'program does not fit so puzzle should not change')
        xword.puzzle = xword.puzzle_copy[:]  # just in case

    def test_fit_word_vertically_another_word_there(self):
        new_puzzle = xword.puzzle[:]
        if xword.fit_word_vertical(0, 5, 'something'):
            xword.put_word('something', 0, 5, 'V')
        self.assertEqual(xword.puzzle, new_puzzle,
                         'testing is already in that location')
        xword.puzzle = xword.puzzle_copy[:]  # just in case


if __name__ == '__main__':
    try:
        unittest.main()
    except SystemExit as inst:
        if inst.args[0] is True:  # raised by sys.exit(True) when tests failed
            raise

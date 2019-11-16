# By: Ilir Dema
# Institution: UTSC

'''
This module should be used to test the parameter and return types of your
functions. 
'''

import xwordAPI as crossword

puzzle = ['python    ', '  e   i   ', '  string  ', '  t   t   ']
width = 10
height = 4

# Type check crossword.is_empty
result = crossword.is_empty(" ")
assert isinstance(result, bool), \
    '''is_empty should return an bool, but returned {0}''' \
    .format(type(result))

# Type check crossword.char_left
result = crossword.char_left(0, 0)
assert isinstance(result, str), \
    '''char_left should return an str, but returned {0}''' \
    .format(type(result))

# Type check crossword.char_right
result = crossword.char_right(0, 0)
assert isinstance(result, str), \
    '''char_right should return an str, but returned {0}''' \
    .format(type(result))

# Type check crossword.char_above
result = crossword.char_above(0, 0)
assert isinstance(result, str), \
    '''char_above should return an str, but returned {0}''' \
    .format(type(result))

# Type check crossword.char_below
result = crossword.char_below(0, 0)
assert isinstance(result, str), \
    '''char_below should return an str, but returned {0}''' \
    .format(type(result))

# Type check crossword.fit_char_horizontal
result = crossword.fit_char_horizontal(0, 0, "s")
assert isinstance(result, bool), \
    '''fit_char_horizontal should return an bool, but returned {0}''' \
    .format(type(result))

# Type check crossword.fit_char_vertical
result = crossword.fit_char_vertical(0, 0, "t")
assert isinstance(result, bool), \
    '''fit_char_vertical should return an bool, but returned {0}''' \
    .format(type(result))

# Type check crossword.put_word(word, row, col, direction)
result = crossword.put_word("p", 0, 0, "V")
assert isinstance(result, type(None)), \
    '''put_word should return a NoneType, but returned {0}''' \
    .format(type(result))


print("If you see this (and no error messages above it), \
then you have passed the type checker")

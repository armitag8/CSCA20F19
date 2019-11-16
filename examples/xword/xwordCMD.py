import xwordAPI as crossword

crossword.width = 19
crossword.height = 8
crossword.puzzle = [" "*crossword.width for x in range(crossword.height)]


def place_word(word, row, column, direction):
    if direction == "H":
        if crossword.fit_word_horizontal(row, column, word):
            crossword.put_word(word, row, column, direction)
    elif direction == "V":
        if crossword.fit_word_vertical(row, column, word):
            crossword.put_word(word, row, column, direction)


place_word("this", 0, 1, "V")
place_word("assignment", 3, 0, "H")
place_word("is", 3, 3, "V")
place_word("too", 0, 1, "H")
place_word("easy", 3, 7, "V")
place_word("next", 3, 5, "V")
place_word("toy", 6, 5, "H")

print(crossword.draw_puzzle())

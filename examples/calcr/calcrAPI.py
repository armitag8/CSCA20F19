#! /usr/bin/env python3

# Constants
ROMAN_TO_DECIMAL = {
    "M": 1000,
    "D": 500,
    "C": 100,
    "L": 50,
    "X": 10,
    "V": 5,
    "I": 1,
}
ROMAN_TO_DECIMAL_L = [(key, value) for key, value in ROMAN_TO_DECIMAL.items()]
DECIMAL_TO_ROMAN_L = [(value, key) for key, value in ROMAN_TO_DECIMAL_L]
DECIMAL_TO_ROMAN = {key: value for key, value in DECIMAL_TO_ROMAN_L}
ROMAN_NUMERALS = [key for key in ROMAN_TO_DECIMAL]
MAX_VALUE = 3499  # I could support up to 4999, but I got lazy implementing.
# Can you tell why my code doesn't work for numbers >= 3500?
OPERATIONS = {
    "+": int.__add__,
    "-": int.__sub__,
    "*": int.__mul__,
    "/": int.__floordiv__,
    "mod": int.__mod__,
    "^": int.__pow__,
}


def compute_roman_expression(roman_1: str, roman_2: str, selected_op: str):
    """
    Returns the Roman number obtained by application of the selected operation
    on the two given Roman numbers.

    Examples:
    >>> compute_roman_expression("MM", "C", "+")
    'MMC'

    >>> compute_roman_expression("MM", "C", "-")
    'MCM'

    >>> compute_roman_expression("XV", "III", "*")
    'XLV'

    >>> compute_roman_expression("X", "V", "+")
    'XV'
    """
    if selected_op not in OPERATIONS:
        print("Invalid operation: " + selected_op)
    else:
        operation = OPERATIONS[selected_op]
        try:
            number_1 = roman_to_decimal(roman_1)
            number_2 = roman_to_decimal(roman_2)
        except ValueError as e:
            print(e)
        else:
            result = operation(number_1, number_2)
            return decimal_to_roman(result)


def _separate_terms_of_roman_number(roman_numerals: str) -> list:
    """
    Separates a Roman number into independent terms.

    Examples:
    >>> _separate_terms_of_roman_number("")
    []

    >>> _separate_terms_of_roman_number("LL")
    ['LL']

    >>> _separate_terms_of_roman_number("VIII")
    ['V', 'III']

    >>> _separate_terms_of_roman_number("CM")
    ['C-M']

    >>> _separate_terms_of_roman_number("CCMLXIV")
    ['CC-M', 'L', 'X', 'I-V']

    >>> _separate_terms_of_roman_number("MCMLVXII")
    ['M', 'C-M', 'L', 'V-X', 'II']
    """
    term = ""
    result = []
    previous = ""

    for character in roman_numerals:

        if character not in ROMAN_NUMERALS:
            raise ValueError("Not a valid Roman numeral: " + character)

        if previous == "" or character == previous:
            term += character
        elif ROMAN_NUMERALS.index(character) < ROMAN_NUMERALS.index(previous):
            # the current numeral is greater than the previous
            term += "-" + character
        elif ROMAN_NUMERALS.index(character) > ROMAN_NUMERALS.index(previous):
            # the current numeral is less than the previous
            result.append(term)
            term = character

        previous = character

    if term:
        result.append(term)

    return result


def _value_of_roman_numeral_terms(roman_numeral_terms: list) -> int:
    """
    Returns the decimal value of the list of Roman numeral terms.

    Examples:
    >>> _value_of_roman_numeral_terms([])
    0

    >>> _value_of_roman_numeral_terms(["CC"])
    200

    >>> _value_of_roman_numeral_terms(["L-C", "II"])
    52
    """
    total = 0
    for term in roman_numeral_terms:
        if term[0] == term[-1]:
            if len(term) > 3:
                raise ValueError("Not a valid Roman number since: " + term)
            total += len(term) * ROMAN_TO_DECIMAL[term[0]]
        else:
            subtract, add = term.split("-")
            if len(subtract) > 2:
                raise ValueError("Not a valid Roman number since: " + term)
            if len(add) > 3:
                raise ValueError("Not a valid Roman number since: " + add)
            total -= len(subtract) * ROMAN_TO_DECIMAL[subtract[0]]
            total += len(add) * ROMAN_TO_DECIMAL[add[0]]

    return total


def roman_to_decimal(roman_number: str) -> int:
    """
    Converts a Roman number to a decimal number.

    REQ: roman_number must be a valid Roman number

    Examples:
    >>> roman_to_decimal("")
    0

    >>> roman_to_decimal("II")
    2

    >>> roman_to_decimal("XLII")
    42

    >>> roman_to_decimal("MCMLXVXII")
    1967
    """
    terms = _separate_terms_of_roman_number(roman_number)
    return _value_of_roman_numeral_terms(terms)


def decimal_to_roman(number: int) -> str:
    """
    Converts a decimal number to its Roman numeral representation.

    REQ: number must be positive and less than MAX_VALUE(4999)

    Examples:
    >>> decimal_to_roman(0)
    ''

    >>> decimal_to_roman(1)
    'I'

    >>> decimal_to_roman(3)
    'III'

    >>> decimal_to_roman(31)
    'XXXI'

    >>> decimal_to_roman(40)
    'XL'

    >>> decimal_to_roman(90)
    'XC'

    >>> decimal_to_roman(1978)
    'MCMLXXIIX'

    >>> decimal_to_roman(3499)
    'MMMCDXCIX'


    >>> decimal_to_roman(41)
    'XLI'

    >>> decimal_to_roman(45)
    'XLV'

    >>> decimal_to_roman(49)
    'XLIX'

    >>> decimal_to_roman(15)
    'XV'

    >>> decimal_to_roman(16)
    'XVI'

    >>> decimal_to_roman(999)
    'CMXCIX'
    """
    if number > MAX_VALUE:
        raise ValueError(
            "Roman numbers cannot exceed {}; but given value is: {}"
            .format(MAX_VALUE, number))

    result = ""
    decimal_place = len(ROMAN_NUMERALS) - 1

    for character in reversed(str(number)):
        digit = int(character)

        if digit < 4:
            result = digit * ROMAN_NUMERALS[decimal_place] + result
        elif digit == 4:
            ones = digit // 3 * ROMAN_NUMERALS[decimal_place]
            fives = ROMAN_NUMERALS[decimal_place - 1]
            result = ones + fives + result
        elif digit < 8:
            ones = (digit - 5) * ROMAN_NUMERALS[decimal_place]
            fives = ROMAN_NUMERALS[decimal_place - 1]
            result = fives + ones + result
        else:  # digit == 9
            tens = ROMAN_NUMERALS[decimal_place - 2]
            ones = (10 - digit) * ROMAN_NUMERALS[decimal_place]
            result = ones + tens + result

        decimal_place -= 2

    return result


def main():
    """
    Just test this API using doctest if this module is run directly.

    Tests:
    >>> ROMAN_TO_DECIMAL_L
    [('M', 1000), ('D', 500), ('C', 100), ('L', 50), ('X', 10), ('V', 5), ('I', 1)]

    >>> DECIMAL_TO_ROMAN_L
    [(1000, 'M'), (500, 'D'), (100, 'C'), (50, 'L'), (10, 'X'), (5, 'V'), (1, 'I')]

    >>> DECIMAL_TO_ROMAN == \
        {1000: 'M', 500: 'D', 100: 'C', 50: 'L', 10: 'X', 5: 'V', 1: 'I'}
    True

    >>> ROMAN_NUMERALS == ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    True
    """
    import doctest
    doctest.testmod(verbose=True)
    input("Does this look OK?")


if __name__ == "__main__":
    main()

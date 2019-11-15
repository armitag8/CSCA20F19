#! /usr/bin/env python3

from calcrAPI import OPERATIONS, compute_roman_expression


def main():
    number1 = input("Input a Roman number: ")
    number2 = input("Input another Roman number: ")
    print("Select an operation from: " + " or ".join(OPERATIONS.keys()))
    operation_selection = input("Select your operation: ")
    result = compute_roman_expression(number1, number2, operation_selection)
    print(result)


if __name__ == "__main__":
    main()

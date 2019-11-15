#! /usr/bin/env python3

import tkinter
from calcrAPI import compute_roman_expression

number1 = ""
number2 = ""
operation = None


def press_numeral(numeral: str):
    global number1, number2
    if operation:
        number2 += numeral
        equation.set(number1 + " " + operation + " " + number2)
    else:
        number1 += numeral
        equation.set(number1)


def press_operation(selected_operation: str):
    global operation
    operation = selected_operation
    equation.set(number1 + " " + operation)


def compute():
    global number1, number2, operation
    if not operation:
        return
    equation.set(compute_roman_expression(number1, number2, operation))
    number1 = ""
    number2 = ""
    operation = None


if __name__ == "__main__":
    window = tkinter.Tk()
    window.title("Roman Calculator")
    window.geometry("270x145")

    equation = tkinter.StringVar()
    expression_field = tkinter.Entry(window, textvariable=equation)
    expression_field.grid(columnspan=4, ipadx=70)

    equation.set('Enter your expression')
    buttonM = tkinter.Button(window, text=' M ',
                             command=lambda: press_numeral("M"), height=1, width=6)
    buttonM.grid(row=2, column=0)

    buttonD = tkinter.Button(window, text=' D ',
                             command=lambda: press_numeral("D"), height=1, width=6)
    buttonD.grid(row=2, column=1)

    buttonC = tkinter.Button(window, text=' C ',
                             command=lambda: press_numeral("C"), height=1, width=6)
    buttonC.grid(row=2, column=2)

    buttonL = tkinter.Button(window, text=' L ',
                             command=lambda: press_numeral("L"), height=1, width=6)
    buttonL.grid(row=3, column=0)

    buttonX = tkinter.Button(window, text=' X ',
                             command=lambda: press_numeral("X"), height=1, width=6)
    buttonX.grid(row=3, column=1)

    buttonV = tkinter.Button(window, text=' V ',
                             command=lambda: press_numeral("V"), height=1, width=6)
    buttonV.grid(row=3, column=2)

    buttonI = tkinter.Button(window, text=' I ',
                             command=lambda: press_numeral("I"), height=1, width=6)
    buttonI.grid(row=4, column=0)

    plus = tkinter.Button(window, text=' + ',
                          command=lambda: press_operation("+"), height=1, width=6)
    plus.grid(row=4, column=1)

    minus = tkinter.Button(window, text=' - ',
                           command=lambda: press_operation("-"), height=1, width=6)
    minus.grid(row=4, column=2)

    multiply = tkinter.Button(window, text=' * ',
                              command=lambda: press_operation("*"), height=1, width=6)
    multiply.grid(row=5, column=1)

    divide = tkinter.Button(window, text=' / ',
                            command=lambda: press_operation("/"), height=1, width=6)
    divide.grid(row=5, column=2)

    equal = tkinter.Button(window, text=' = ',
                           command=compute, height=1, width=6)
    equal.grid(row=5, column=0)
    window.mainloop()

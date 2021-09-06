# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

'''

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

'''
def fnNumerate(lstNumberDigits):
    # This function creates an integer from a list of digits
    # print(lstNumberDigits)
    intNumber = 0
    for intCtr, chrDigit in enumerate(lstNumberDigits):
        intNumber += chrDigit * pow(10, intCtr)
    return(intNumber)

# This program builds a list of 10-digit random numbers and in each number, a digit only appears once

lstDigits = list(range(10))
lstNumbers = []
intNumbers = 20
for intCtr in range(intNumbers):
    lstThisNumber = lstDigits
    random.seed()
    random.shuffle(lstThisNumber)
    intNumber = fnNumerate(lstThisNumber)
    lstNumbers.append(intNumber)
print(lstNumbers)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

# find_min_n2.py
import math


def find_min_n2(numberList):
    """
    Find the minimum number in a list of numbers.
    
    Keyword arguments:
    numberList -- the list of numbers
    
    Returns:
    min -- the minimum number from numberList
    """
    min = math.inf
    # Loop through every number
    for number1 in numberList:
        is_min = True
        # Compare number1 with every other number in numberList
        for number2 in numberList:
            # If number1 is larger than any other number, then it's not min
            if number1 > number2:
                is_min = False
        # If the minimum number is found, return
        if is_min == True:
            min = number1
            return min
    return min

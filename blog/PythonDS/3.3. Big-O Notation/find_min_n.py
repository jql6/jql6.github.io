# find_min_n.py
import math


def find_min_n(numberList):
    """
    Find the minimum number in a list of numbers
    
    Keyword arguments:
    numberList -- the list of numbers
    
    Returns:
    min -- the minimum number from numberList
    """
    min = math.inf
    for number in numberList:
        if number < min:
            min = number
    return min

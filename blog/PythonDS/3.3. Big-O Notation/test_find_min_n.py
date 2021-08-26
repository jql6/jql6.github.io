# test_find_min_n.py
# Python 3.8.5
import unittest
import math
from find_min_n import find_min_n


class TestMinFunction(unittest.TestCase):
    def test_it_returns_min_number(self):
        array1 = [3, 4, 10, 6, 5]
        minimum_number1 = min(array1)
        array2 = [4, 6, 7, 9, 4, 4, 4]
        minimum_number2 = min(array2)
        self.assertEqual(find_min_n(array1), minimum_number1)
        self.assertEqual(find_min_n(array2), minimum_number2)

    def test_it_handles_empty_lists(self):
        self.assertEqual(find_min_n([]), math.inf)

    def test_it_handles_lists_with_one_element(self):
        self.assertEqual(find_min_n([-1]), -1)


# Run the unit tests if this script is called by name in the terminal
if __name__ == "__main__":
    unittest.main()

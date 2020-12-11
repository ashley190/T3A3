import unittest
from main import add


class TestMathFunctions(unittest.TestCase):
    def test_add(self):
        result = add(1, 5)

        if result != 6:
            raise Exception("Add did not bring back 6 when given 1 and 5")

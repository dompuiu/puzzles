from unittest import TestCase
from grid_path.factorial import factorial


class TestFactorial(TestCase):
    def test_zero_factorial(self):
        self.assertEquals(factorial(0), 1)

    def test_one_factorial(self):
        self.assertEquals(factorial(1), 1)

    def test_two_factorial(self):
        self.assertEquals(factorial(2), 2)

    def test_five_factorial(self):
        self.assertEquals(factorial(3), 6)

    def test_factorial_on_negative(self):
        """factorial should fail with negative input"""
        self.assertRaises(Exception, factorial, -1)

    def test_factorial_on_nonnumber(self):
        self.assertRaises(TypeError, factorial, "saa")
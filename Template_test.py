import unittest
import math
import numpy as np
# Import the script you want to test here, so you can use its variables/functions below

class MyTestCase(unittest.TestCase):

    # Add tests you want to run here. Make sure you clearly define and justify (Somewhere) the variables used
    # Delete sample tests shown below:
    # All test function names should start with 'test', otherwise they will not run!
    def test_integers(self):
        a = 5
        b = 5
        self.assertEqual(a, b)

    def test_floats(self):
        a = 5.
        b = 5.0001
        digits = 3 # To what digit will the floats be compared?
        self.assertAlmostEqual(a, b, places = digits)

    def test_string(self):
        a = "This test will fail"
        b = "This test will failll"
        self.assertEqual(a, b)


if __name__ == '__main__':
    unittest.main()
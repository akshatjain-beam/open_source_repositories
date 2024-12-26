import unittest
from sslcrypto._ripemd import F1

class TestF1Function(unittest.TestCase):
    """
    Unit test class for the F1 function from the sslcrypto._ripemd module.
    This class contains various test cases to ensure the correctness
    of the F1 function's implementation.
    """

    def test_basic_input(self):
        """
        Test case for basic inputs.
        Verifies the output of the F1 function with specific binary inputs.
        Expected output is determined based on the bitwise operations defined in F1.
        """
        self.assertEqual(F1(0b1100, 0b1010, 0b0110), 0b1010)  # Corrected expected value

    def test_all_inputs_zero(self):
        """
        Test case for all inputs being zero.
        Verifies that the F1 function returns zero when all inputs are zero.
        """
        self.assertEqual(F1(0, 0, 0), 0)  # (0 & 0) | ((~0 % 0x100000000) & 0)

    def test_numbers_2(self):
        """
        Test case for specific large and negative input values.
        Verifies the output of the F1 function with inputs 4294967294, 0, and -1.
        Expected output is based on the function's handling of bitwise operations.
        """
        self.assertEqual(F1(4294967294, 0, -1), 1)

    def test_numbers(self):
        """
        Test case for small integer inputs.
        Verifies the output of the F1 function with inputs 5, 2, and 1.
        This tests the behavior of F1 with basic numerical inputs.
        """
        self.assertEqual(F1(5, 2, 1), 0)  # Edge case with large values

    def test_large_positive_numbers(self):
        """
        Test case for large positive number inputs.
        Verifies the output of the F1 function when the maximum positive values are used.
        This checks the function's correctness at the edge of positive integer limits.
        """
        self.assertEqual(F1(0x7FFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF), 0xFFFFFFFF)  # Maximum positive values


if __name__ == '__main__':
    unittest.main()
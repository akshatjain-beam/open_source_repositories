import unittest
from sslcrypto._ripemd import ROL

class TestROLFunction(unittest.TestCase):

    def test_rol_1(self):
        """
        Test a simple left rotation by 1 bit on the integer 1.
        The expected output is 2 (binary: 0b10), as the bit shifts
        one position to the left, and 0 fills in from the right.
        """
        self.assertEqual(ROL(1, 0b00000000000000000000000000000001), 0b00000000000000000000000000000010)

    def test_rol_2(self):
        """
        Test a left rotation by 2 bits on the integer 1.
        The expected output is 4 (binary: 0b100). The leftmost bit
        shifts to the left, and two 0 bits fill in from the right.
        """
        self.assertEqual(ROL(2, 0b00000000000000000000000000000001), 0b00000000000000000000000000000100)

    def test_rol_3(self):
        """
        Test a left rotation by 3 bits on the integer 8 (binary: 0b00001000).
        The expected output is 64 (binary: 0b1000000). The leftmost bit overflows
        and wraps around to the rightmost position.
        """
        self.assertEqual(ROL(3, 0b00000000000000000000000000001000), 0b00000000000000000000000001000000)

    def test_rol_full_rotation(self):
        """
        Test a left rotation by 32 bits on the integer 0xFFFFFFFF.
        Since rotating by the bit width of the integer should yield
        the same value, the expected output is 0xFFFFFFFF.
        """
        self.assertEqual(ROL(32, 0xFFFFFFFF), 0xFFFFFFFF)

    def test_rol_5(self):
        """
        Test the ROL function for a left rotation of a negative integer.
        This test case checks the behavior of the ROL function when the input integer
        is negative.
        """
        self.assertEqual(ROL(4,-16 ), -1)  

if __name__ == '__main__':
    unittest.main()

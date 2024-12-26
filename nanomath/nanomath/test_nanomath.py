import unittest
import numpy as np
from nanomath.nanomath import get_N50  # Import the get_N50 function

class TestGetN50(unittest.TestCase):
    """Unit tests for the get_N50 function in the nanomath module."""

    def test_basic_case(self):
        """Test N50 calculation with a standard input of mixed read lengths."""
        readlengths = np.array([100, 200, 300, 400])
        result = get_N50(readlengths)
        self.assertEqual(result, 300)  # 300 is the N50 for this dataset

    def test_case_with_one_read(self):
        """Test N50 calculation when there is only one read."""
        readlengths = np.array([500])
        result = get_N50(readlengths)
        self.assertEqual(result, 500)  # N50 should be the length itself

    def test_case_with_two_reads(self):
        """Test N50 calculation with two reads of different lengths."""
        readlengths = np.array([100, 400])
        result = get_N50(readlengths)
        self.assertEqual(result, 400)  # N50 should be the longer read

    def test_case_with_same_length_reads(self):
        """Test N50 calculation when all reads have the same length."""
        readlengths = np.array([200, 200, 200])
        result = get_N50(readlengths)
        self.assertEqual(result, 200)  # N50 for identical lengths should be the same length

    def test_large_numbers(self):
        """Test N50 calculation with large identical read lengths."""
        readlengths = np.array([1_000_000, 1_000_000, 1_000_000, 1_000_000, 1_000_000])
        result = get_N50(readlengths)
        self.assertEqual(result, 1_000_000)  # N50 for large identical lengths should be the same length

    def test_case_with_fractional_N50(self):
        """Test N50 calculation when the longest read influences the result."""
        readlengths = np.array([100, 100, 300])
        result = get_N50(readlengths)
        self.assertEqual(result, 300)  # N50 should still be the longest read

if __name__ == '__main__':
    unittest.main()

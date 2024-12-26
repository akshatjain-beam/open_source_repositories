import unittest
import pandas as pd
import numpy as np
from nanomath.nanomath import remove_length_outliers

class TestRemoveLengthOutliers(unittest.TestCase):

    def setUp(self):
        """
        Set up sample data for testing.
        This method runs before each test case.
        """
        self.df = pd.DataFrame({
            'lengths': [1, 1,1,1,1,1,1,1,1,2,3, 101]  
        })

    def test_remove_outlier(self):
        """
        Test that the function correctly removes the outlier (101) from the DataFrame.
        """
        result = remove_length_outliers(self.df, 'lengths')
        self.assertNotIn(101, result['lengths'].values)

    def test_no_outlier(self):
        """
        Test that the function returns the same DataFrame when no outliers exist.
        """
        df_no_outliers = pd.DataFrame({
            'lengths': [10, 12, 13, 14, 15]
        })
        result = remove_length_outliers(df_no_outliers, 'lengths')
        np.testing.assert_array_equal(result['lengths'].values, df_no_outliers['lengths'].values)


    def test_below_threshold_outliers(self):
        """
        Test that the function correctly handles values below the outlier threshold.
        """
        df_below_threshold = pd.DataFrame({
            'lengths': [-101,-3,-2,-1,-1,-1,-1,1, 1,1,1,1,1,1,1,1,2,3]  
        })
        result = remove_length_outliers(df_below_threshold, 'lengths')
        np.testing.assert_array_equal(result['lengths'].values, [-101, -3, -2, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])

    def test_above_outliers(self):
        """
        Test that the function correctly handles all values below the threshold.
        """
        df_only_below_outliers = pd.DataFrame({
            'lengths': [-1,-1,1, 1,1,1,1,1,1,1,1,2,3, 101]  
        })
        result = remove_length_outliers(df_only_below_outliers, 'lengths')
        np.testing.assert_array_equal(result['lengths'].values, [-1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])

    def test_above_below_outlier(self):
        """
        Test that the function correctly handles both above and below outliers.
        """
        data = pd.DataFrame({'lengths': [-101,-3,-2,-1,-1,-1,-1,1, 1,1,1,1,1,1,1,1,2,3, 101]})
        result = remove_length_outliers(data, 'lengths')
        np.testing.assert_array_equal(result['lengths'].values, [-101, -3, -2, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3])
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

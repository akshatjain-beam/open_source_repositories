from nanomath.nanomath import get_top_5

import pandas as pd
import unittest
import pandas as pd
import numpy as np
from nanomath.nanomath import remove_length_outliers

class TestRemoveLengthOutliers(unittest.TestCase):

class TestGetTop5Function(unittest.TestCase):
    """Unit tests for the get_top_5 function."""

    def setUp(self):
        """Set up sample DataFrame for testing."""
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'readIDs': ['id1', 'id2', 'id3', 'id4', 'id5']
        })

    def test_get_top_5_with_fill(self):
        """Test get_top_5 function with fill=True."""
        result = get_top_5(self.df, 'B', ['A', 'B'], fill=True)
        expected = [(1, 5, 'id1', 0), (2, 4, 'id2', 0), (3, 3, 'id3', 0), (4, 2, 'id4', 0), (5, 1, 'id5', 0)]
        self.assertEqual(list(result), expected)

    def test_get_top_5_without_fill(self):
        """Test get_top_5 function with fill=False."""
        result = get_top_5(self.df, 'B', ['A', 'B'], fill=False)
        expected = [(1, 5, 'id1'), (2, 4, 'id2'), (3, 3, 'id3'), (4, 2, 'id4'), (5, 1, 'id5')]
        self.assertEqual(list(result), expected)

    def test_get_top_5_with_readIDs(self):
        """Test get_top_5 function with readIDs."""
        result = get_top_5(self.df, 'A', ['B'], fill=False)
        expected = [(1, 'id5'), (2, 'id4'), (3, 'id3'), (4, 'id2'), (5, 'id1')]
        self.assertEqual(list(result), expected)

    def test_get_top_5_empty_dataframe(self):
        """Test get_top_5 function with an empty DataFrame."""
        empty_df = pd.DataFrame(columns=['A', 'B', 'readIDs'])
        result = get_top_5(empty_df, 'B', ['A', 'B'], fill=False)
        expected = []
        self.assertEqual(list(result), expected)

    def test_get_top_5_no_columns(self):
        """Test get_top_5 function with a DataFrame with no relevant columns."""
        df_no_columns = pd.DataFrame(columns=['A', 'B'])
        result = get_top_5(df_no_columns, 'B', ['A'], fill=False)
        expected = []
        self.assertEqual(list(result), expected)

    def test_get_top_5_new_function_with_fill_string(self):
        """Test get_top_5 function with checking default value of fill."""
        result = get_top_5(self.df, 'B', ['A', 'B'])
        expected = [(1, 5, 'id1'), (2, 4, 'id2'), (3, 3, 'id3'), (4, 2, 'id4'), (5, 1, 'id5')]
        self.assertEqual(list(result), expected)

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

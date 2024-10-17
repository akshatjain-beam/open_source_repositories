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

if __name__ == '__main__':
    unittest.main()

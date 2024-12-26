import pandas as pd
import unittest
from typing import List
from py2mappr._attributes.utils import find_node_color_attr

class TestFindNodeColorAttr(unittest.TestCase):
    """
    Unit tests for the find_node_color_attr function.

    This test suite checks the functionality of the `find_node_color_attr` 
    function to identify the most suitable column to be used as the color 
    attribute for nodes in a graph based on distinct values and null counts.
    """

    def setUp(self):
        """
        Set up the test case environment.
        
        This method runs before each individual test case. 
        Currently, it doesn't perform any setup actions but can be 
        extended in the future if needed.
        """
        pass

    def test_multiple_columns(self):
        """
        Test case to check the behavior with multiple columns of different types.
        
        In this test, column 'B' is expected to be returned as it has the 
        least distinct values (0) when compared to other columns.
        """
        df = pd.DataFrame({
            'A': [1, 2, 2, None],
            'B': [1, None, None, None],
            'C': ['red', 'blue', 'green', 'red']
        })
        result = find_node_color_attr(df)
        self.assertEqual(result, 'B')  # B has the fewest unique values (0)

    def test_multiple_columns_same_unique_values(self):
        """
        Test case to check the behavior when multiple columns have the same 
        number of unique values.
        
        This test checks if the function can handle a scenario where all 
        columns have the same number of unique values. It should return one 
        of them.
        """
        df = pd.DataFrame({
            'A': [1, 2, 1, 1],
            'B': [2, 2, 2, 2],
            'C': [3, 3, 3, 3]
        })
        result = find_node_color_attr(df)
        self.assertIn(result, ['A', 'B', 'C'])  # All have the same unique values

    def test_all_missing_column(self):
        """
        Test case to check the behavior when all values in a column are missing.
        
        In this scenario, column 'A' has no unique values, and should be 
        returned as the most suitable column for color attributes.
        """
        df = pd.DataFrame({
            'A': [None, None, None, None],
            'B': [1, 2, 3, None],
            'C': ['red', 'blue', 'green', None]
        })
        result = find_node_color_attr(df)
        self.assertEqual(result, 'A')  # A has the fewest unique values (0)

    def test_single_column(self):
        """
        Test case to check the behavior with a single column.
        
        This tests the simplest case where only one column is present in 
        the DataFrame. It should return that column as the result.
        """
        df = pd.DataFrame({
            'A': [1, 2, 2, 1]
        })
        result = find_node_color_attr(df)
        self.assertEqual(result, 'A')  # Only one column present

    def test_all_unique_columns(self):
        """
        Test case to check the behavior when all columns have unique values.
        
        In this case, since each column has distinct values, the function 
        should return one of them.
        """
        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [4, 5, 6],
            'C': ['red', 'green', 'blue']
        })
        result = find_node_color_attr(df)
        self.assertIn(result, ['A', 'B', 'C'])  # Any of the columns could be returned

if __name__ == '__main__':
    unittest.main()
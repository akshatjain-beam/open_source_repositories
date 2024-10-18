from nanomath.nanomath import get_top_5

import pandas as pd
import unittest


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



if __name__ == '__main__':
    unittest.main()

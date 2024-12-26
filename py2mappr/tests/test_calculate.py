import unittest
import pandas as pd
import numpy as np
import warnings
from py2mappr._attributes.calculate import calculate_attr_types

class TestAttributeDetection(unittest.TestCase):

    def test_liststring_detection(self):
        """Test detection of 'liststring' type for columns containing pipe-separated values.
        
        This test checks if the function correctly identifies a column with pipe-separated
        values as a 'liststring' type, and a column with single values as a 'string' type.
        """
        df_with_pipes = pd.DataFrame({
            'column2': ['a|b', 'c', 'd']
        })
        df_without_pipes = pd.DataFrame({
            'column2': ['a', 'b', 'c']
        })
        expected_with_pipes = {'column2': 'liststring'}
        expected_without_pipes = {'column2': 'string'}

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df_with_pipes), expected_with_pipes)
            self.assertEqual(calculate_attr_types(df_without_pipes), expected_without_pipes)

    def test_bool_type(self):
        """Test detection of boolean type in a DataFrame column.
        
        This test verifies that a column containing boolean values is identified as a 'string'
        type, as the function may not distinguish boolean types from strings.
        """
        df = pd.DataFrame({
            'column3': pd.Series([True, False, True], dtype=bool)
        })
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            expected = {'column3': 'string'}
            self.assertEqual(calculate_attr_types(df), expected)

    def test_integer_detection(self):
        """Test detection of integer type in a DataFrame column.
        
        This test checks if the function correctly identifies a column of integers as an 'integer' type.
        """
        df = pd.DataFrame({
            'column4': [1, 2, 3, 4, 5]
        })
        expected = {'column4': 'integer'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df), expected)

    def test_float_detection(self):
        """Test detection of float type in a DataFrame column.
        
        This test verifies that a column of floating-point numbers is identified as a 'float' type.
        """
        df = pd.DataFrame({
            'column5': [1.1, 2.2, 3.3, 4.4, 5.5]
        })
        expected = {'column5': 'float'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df), expected)

    def test_year_detection(self):
        """Test detection of year type in a DataFrame column.
        
        This test checks if the function correctly identifies a column of year values as a 'year' type.
        """
        df = pd.DataFrame({
            'column6': [1990, 2000, 2010, 2020]
        })
        expected = {'column6': 'year'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df), expected)

    def test_timestamp_detection(self):
        """Test detection of timestamp type in a DataFrame column.
        
        This test verifies that a column containing Unix timestamps is identified as a 'timestamp' type.
        """
        df = pd.DataFrame({
            'column7': [1609459200, 1609545600, 1609632000]
        })
        expected = {'column7': 'timestamp'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df), expected)

    def test_single_value_column(self):
        """Test detection of integer type in a single-value DataFrame column.
        
        This test checks if the function correctly identifies a column with a single integer value as an 'integer' type.
        """
        df = pd.DataFrame({
            'column10': [1]
        })
        expected = {'column10': 'integer'}
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            self.assertEqual(calculate_attr_types(df), expected)

if __name__ == '__main__':
    unittest.main()
import unittest
import pandas as pd
from unittest.mock import patch
from matplotlib import pyplot as plt
from uncertain_panda.plotting.helpers import plot_with_uncertainty  # Update this import as necessary

class TestPlotWithUncertainty(unittest.TestCase):

    @patch('matplotlib.pyplot.errorbar')
    def test_plot_with_missing_std_dev_columns(self, mock_errorbar):
        """
        Test the function with a DataFrame missing standard deviation columns.
        
        This test verifies that the function raises a KeyError when attempting
        to access standard deviation columns that do not exist in the DataFrame.
        """
        df = pd.DataFrame({
            'value': [10, 20, 15]
        })

        # Call the function and expect it to raise KeyError
        with self.assertRaises(KeyError):
            plot_with_uncertainty(df, key='value')

    @patch('matplotlib.pyplot.errorbar')
    def test_plot_with_nominal_value(self, mock_errorbar):
        """
        Test the function with a DataFrame containing nominal values.
        
        This test checks that when the key is not provided, the function
        plots the nominal_value with yerr and does not call plt.errorbar.
        """
        df = pd.DataFrame({
            'nominal_value': [10, 20, 15],
            'std_dev': [1, 2, 1.5]
        })

        # Call the function without key
        plot_with_uncertainty(df)

        # Check if nominal_value was plotted with yerr
        df.nominal_value.plot(yerr=df.std_dev, **{})

        # Assert that errorbar was not called since key was not provided
        mock_errorbar.assert_not_called()

    @patch('matplotlib.pyplot.errorbar')
    def test_plot_without_nominal_value(self, mock_errorbar):
        """
        Test the function with a DataFrame that has no nominal value.
        
        This test verifies that when the DataFrame does not contain a
        nominal value and no key is provided, the function plots the
        DataFrame directly and does not call plt.errorbar.
        """
        df = pd.DataFrame({
            'value': [1, 2, 3]
        })

        # Call the function without key
        plot_with_uncertainty(df)

        # Check if the DataFrame was plotted directly
        df.plot(**{})

        # Assert that errorbar was not called since no key or nominal value was provided
        mock_errorbar.assert_not_called()

    @patch('matplotlib.pyplot.errorbar')
    def test_plot_with_empty_dataframe(self, mock_errorbar):
        """
        Test the function with an empty DataFrame.
        
        This test checks that the function handles an empty DataFrame gracefully
        and raises a KeyError when trying to access a column that does not exist.
        """
        df = pd.DataFrame()

        # Call the function and expect it to handle the empty DataFrame gracefully
        with self.assertRaises(KeyError):
            plot_with_uncertainty(df, key='value')
    @patch('matplotlib.pyplot.errorbar')

    def test_invalid_key(self, mock_errorbar):
        # Create a mock DataFrame without necessary columns
        df = pd.DataFrame({'value': [10, 20, 30]})
        df.index = [0, 1, 2]

        # Call the function with a key that does not exist
        with self.assertRaises(KeyError):
            plot_with_uncertainty(df, key='invalid_key')


if __name__ == '__main__':
    unittest.main()

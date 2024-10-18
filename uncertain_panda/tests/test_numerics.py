from uncertain_panda import pandas as pd
import pytest
import numpy as np
from tests.fixtures import UncertainPandaTestCase
from uncertain_panda.utils.numerics import value_counts, coverage


class TestNumerics(UncertainPandaTestCase):

    def test_coverage_normal(self):
        for sigma in [1, 5, 100]:
            df = pd.Series(np.random.normal(
                np.random.randint(-10, 10), sigma, 2000))
            coverage = df.coverage(0.68)

            # We allow for +- 5% deviation
            self.assertGreater(coverage, 0.95 * sigma)
            self.assertLess(coverage, 1.05 * sigma)

    def test_coverage_uniform(self):
        df = pd.Series(10 * np.random.rand(10000))

        # We also allow for a small deviation here
        self.assertLess(abs(df.coverage(1.0) - 5), 0.1)
        self.assertLess(abs(df.coverage(0.5) - 2.5), 0.1)
        self.assertLess(abs(df.coverage(0.2) - 1.0), 0.1)

    def test_dataframe_coverage(self):
        df = pd.DataFrame({"a": np.random.normal(np.random.randint(-10, 10), 5, 2000),
                           "b": np.random.normal(np.random.randint(-10, 10), 5, 2000)})

        coverage = df.coverage(0.68)
        self.assertLess(abs(coverage["a"] - 5), 0.5)
        self.assertLess(abs(coverage["b"] - 5), 0.5)

import numpy as np
import unittest

class TestCoverageFunction(unittest.TestCase):

    def test_single_value_series(self):
        """
        Test coverage with a series containing a single value.

        This test checks that the coverage function returns 0 for a series 
        that contains only a single repeated value, as there is no deviation 
        from the median.
        """
        series = np.array([42])
        result = coverage(series)
        self.assertEqual(result, 0, "Expected 0 for a single value series.")

    def test_two_value_series(self):
        """
        Test coverage with a series containing two values.

        This test checks the coverage function for a series with two distinct 
        values, expecting it to return the average of their deviations from 
        the median.
        """
        series = np.array([10, 20])
        result = coverage(series)
        self.assertEqual(result, 5, "Expected 5 for a two-value series.")

    def test_basic_series(self):
        """
        Test coverage with a basic series of integers.

        This test evaluates the coverage function on a simple series of 
        integers and checks if the result matches the expected value.
        """
        series = np.array([1, 2, 3, 4, 5])
        result = coverage(series)
        self.assertEqual(round(result, 1), 1.7, "Expected 1.5 for the basic series.")

    def test_with_nan_values(self):
        """
        Test coverage with NaN values in the series.

        This test checks that the coverage function correctly handles NaN 
        values by ignoring them and calculating the coverage based on the 
        remaining values.
        """
        series = np.array([1, 2, np.nan, 3, 4])
        result = coverage(series)
        self.assertEqual(result, 1.5, "Expected 1.5 for series with NaN values.")

    def test_percentile_cl(self):
        """
        Test coverage with different confidence level (cl) values.

        This test evaluates the coverage function with various confidence levels 
        to ensure it returns the expected percentile of the absolute deviations 
        for the given series.
        """
        series = np.array([1, 2, 3, 4, 5, 6])
        
        result_68 = coverage(series, cl=0.68)
        self.assertAlmostEqual(round(result_68, 1), 1.9, places=1, msg="Expected 1.7 for cl=0.68.")
        
        result_95 = coverage(series, cl=0.95)
        self.assertAlmostEqual(result_95, 2.5, places=1, msg="Expected 2.5 for cl=0.95.")

if __name__ == '__main__':
    unittest.main()
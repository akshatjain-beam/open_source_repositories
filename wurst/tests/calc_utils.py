import unittest
import numpy as np
from wurst.IMAGE.calc_utils import relative_change

class TestRelativeChange(unittest.TestCase):
    """
    Unit tests for the relative_change function from wurst.IMAGE.calc_utils.
    
    The relative_change function calculates the fractional change values from 
    a starting year to an ending year, normalizing by the starting value. 
    These tests ensure that the function works correctly with different shapes 
    and types of input data.
    """

    def test_1d_array(self):
        """
        Test the relative_change function with a 1D array.

        This test checks if the function correctly calculates the 
        fractional change from the year 2000 to the year 2003 
        for a 1D dataset.
        """
        dataset = np.array([10, 20, 30, 40])
        years = [2000, 2001, 2002, 2003]
        start = 2000
        end = 2003
        result = relative_change(dataset, years, start, end)
        expected = 3.0
        self.assertAlmostEqual(result, expected)

    def test_2d_array(self):
        """
        Test the relative_change function with a 2D array.

        This test checks if the function correctly calculates the 
        fractional change from the year 2000 to the year 2003 
        for each row in a 2D dataset.
        """
        dataset = np.array([[10, 20, 30, 40],
                            [50, 60, 70, 80]])
        years = [2000, 2001, 2002, 2003]
        start = 2000
        end = 2003
        result = relative_change(dataset, years, start, end)
        expected = np.array([3.0, 0.6])
        np.testing.assert_almost_equal(result, expected)

    def test_3d_array(self):
        """
        Test the relative_change function with a 3D array.

        This test checks if the function correctly calculates the 
        fractional change from the year 2000 to the year 2001 
        for each element in a 3D dataset.
        """
        dataset = np.array([[[10, 20], [30, 40]],
                            [[50, 60], [70, 80]]])
        years = [2000, 2001]
        start = 2000
        end = 2001
        result = relative_change(dataset, years, start, end)
        expected = np.array([[1.0, 0.33333333],
                             [0.2, 0.14285714]])
        np.testing.assert_almost_equal(result, expected)

    def test_start_equals_end(self):
        """
        Test the relative_change function when start and end years are the same.

        This test checks if the function returns 0.0 when the start year 
        is equal to the end year, indicating no change.
        """
        dataset = np.array([10, 20, 30, 40])
        years = [2000, 2001, 2002, 2003]
        start = 2002
        end = 2002
        result = relative_change(dataset, years, start, end)
        expected = 0.0
        self.assertAlmostEqual(result, expected)

    def test_year_iterable(self):
        """
        Test the relative_change function with years provided as a NumPy array.

        This test checks if the function works correctly when the years 
        are given as a NumPy array instead of a list.
        """
        dataset = np.array([10, 20, 30, 40])
        years = np.array([2000, 2001, 2002, 2003])
        start = 2002
        end = 2002
        result = relative_change(dataset, years, start, end)
        expected = 0.0
        self.assertAlmostEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

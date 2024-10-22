import unittest
import numpy as np
from wurst.IMAGE.calc_utils import convert_to_location_dictionary
from wurst.IMAGE import REGIONS
import numpy.testing as npt


class TestConvertToLocationDictionary(unittest.TestCase):

    def setUp(self):
        """Set up test data for use in tests.
        
        This method initializes various test datasets that will be used 
        throughout the test cases to validate the functionality of 
        the `convert_to_location_dictionary` function. This includes
        one-dimensional and two-dimensional numpy arrays, an empty array,
        and custom region lists.
        """
        self.regions = ['Region A', 'Region B', 'Region C']
        self.empty_array = np.array([])
        self.one_d_array = np.array([10, 20, 30])
        self.two_d_array = np.array([[10, 11], [20, 21], [30, 31]])
        self.large_array = np.array([10, 20, 30, 40])
        self.large_regions = ['Region A', 'Region B', 'Region C', 'Region D']

    def test_convert_one_d_array(self):
        """Test conversion with a 1D array and default regions.
        
        This test checks if the `convert_to_location_dictionary` function
        correctly maps the values from a one-dimensional array to predefined 
        regions (RUS, CHN, RSAF). The test validates that the output dictionary 
        matches the expected values based on the input array.
        """
        expected = {
            'RUS': 10,
            'CHN': 20,
            'RSAF': 30,
        }
        result = convert_to_location_dictionary(self.one_d_array, REGIONS)
        self.assertEqual(result, expected)

    def test_convert_two_d_array(self):
        """Test conversion with a 2D array and default regions.
        
        This test evaluates the behavior of the `convert_to_location_dictionary` 
        function when it receives a two-dimensional array. It ensures that each 
        region is accurately mapped to its corresponding array values, confirming 
        that the function handles multi-dimensional data correctly. The test uses 
        `numpy.testing.assert_array_equal` to verify the output arrays match the 
        expected values.
        """
        expected = {
            'RUS': np.array([10, 11]),
            'CHN': np.array([20, 21]),
            'RSAF': np.array([30, 31]),
        }
        result = convert_to_location_dictionary(self.two_d_array, REGIONS)
        for key in result:
            npt.assert_array_equal(result[key], expected[key])

    def test_convert_with_empty_array(self):
        """Test conversion with an empty array.
        
        This test checks the function's response when provided with an empty 
        array. The expectation is that the function returns an empty dictionary, 
        indicating that it correctly handles edge cases without raising errors.
        """
        expected = {}
        result = convert_to_location_dictionary(self.empty_array, REGIONS)
        self.assertEqual(result, expected)

    def test_convert_with_custom_locations(self):
        """Test conversion with custom locations.
        
        This test examines how the `convert_to_location_dictionary` function 
        behaves when provided with custom region names instead of the default. 
        It ensures that the output dictionary accurately reflects the mapping of 
        the one-dimensional input array values to the specified custom regions, 
        thereby validating the flexibility of the function.
        """
        expected = {
            'Region A': 10,
            'Region B': 20,
            'Region C': 30,
        }
        result = convert_to_location_dictionary(self.one_d_array, self.regions)
        self.assertEqual(result, expected)

    def test_convert_two_d_array_with_custom_locations(self):
        """Test conversion of a 2D array with custom locations.
        
        This test verifies that the `convert_to_location_dictionary` function 
        can handle two-dimensional arrays when custom region names are provided. 
        It checks that the output correctly maps each custom region to its 
        corresponding array values, ensuring the function works seamlessly 
        with different input shapes and region specifications.
        """
        expected = {
            'Region A': np.array([10, 11]),
            'Region B': np.array([20, 21]),
            'Region C': np.array([30, 31]),
        }
        result = convert_to_location_dictionary(self.two_d_array, self.regions)
        for key in result:
            npt.assert_array_equal(result[key], expected[key])


if __name__ == '__main__':
    unittest.main()
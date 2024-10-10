from autuacoes.cities import get_city
import unittest

class TestGetCity(unittest.TestCase):
    """Unit tests for the get_city function to ensure it handles various input scenarios correctly."""

    def test_get_city_with_state_and_city(self):
        """
        Test the get_city function with a valid state abbreviation and city name.
        
        This test verifies that the function correctly returns the state, 
        city, and city IBGE code for a known city when provided with 
        both a state abbreviation and a city name.
        """
        state = "SP"
        city = "São Paulo"
        result = get_city(state, city)
        self.assertEqual(result[0], "SP")  # Check that the state returned is correct
        self.assertEqual(result[1], "São Paulo")  # Check that the city returned is correct
        self.assertIsInstance(result[2], str)  # Ensure city_ibge_code is a string

    def test_get_city_with_city_and_state_in_city_string(self):
        """
        Test the get_city function when the city name includes the state as a suffix.
        
        This test checks if the function can correctly extract and return 
        the state and city information when the input format is 'City/State'.
        """
        city = "São Paulo/SP"
        result = get_city("", city)
        self.assertEqual(result[0], "SP")  # Check that the state returned is correct
        self.assertEqual(result[1], "São Paulo")  # Check that the city returned is correct
        self.assertIsInstance(result[2], str)  # Ensure city_ibge_code is a string

    def test_get_city_with_conflicting_state(self):
        """
        Test the get_city function for handling conflicting state information.
        
        This test ensures that a ValueError is raised when the city string 
        includes a different state than the one provided as an argument. 
        The test checks if the function correctly identifies the conflict.
        """
        state = "RJ"
        city = "São Paulo/SP"
        with self.assertRaises(ValueError):  # Expecting a ValueError due to state conflict
            get_city(state, city)

    def test_get_city_with_unknown_city(self):
        """
        Test the get_city function when querying for a city that does not exist.
        
        This test verifies that a ValueError is raised when the city name 
        provided is not found in the database. This ensures that the function 
        correctly handles invalid city inputs.
        """
        state = "SP"
        city = "Unknown City"
        with self.assertRaises(ValueError):  # Expecting a ValueError for an unknown city
            get_city(state, city)

    def test_city_with_state_in_city_name(self):
        """
        Test the get_city function with a city name that includes the state as part of the name.
        
        This test checks if the function can correctly return the state, 
        city, and city IBGE code when the city name is formatted as 'City/State'.
        """
        state, city, ibge_code = get_city('', 'Florianópolis/SC')
        self.assertEqual(state, 'SC')  # Check that the state returned is correct
        self.assertEqual(city, 'Florianópolis')  # Check that the city returned is correct
        self.assertEqual(ibge_code, '4205407')  # Check the correct IBGE code for the city

if __name__ == "__main__":
    unittest.main()

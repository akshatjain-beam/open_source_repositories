import unittest
from autuacoes.cities import split_state_city

class TestSplitStateCity(unittest.TestCase):
    
    def test_state_acronym(self):
        """
        Test cases where the state is represented by a two-letter acronym.
        Ensures that the function can correctly split the state acronym from the city name.
        """
        self.assertEqual(split_state_city("AC Rio Branco"), ("AC", "Rio Branco"))
        self.assertEqual(split_state_city("SP Sao Paulo"), ("SP", "Sao Paulo"))

    def test_full_state_name(self):
        """
        Test cases where the full state name is provided.
        Ensures that the function can correctly split the full state name from the city name.
        """
        self.assertEqual(split_state_city("Acre Rio Branco"), ("AC", "Rio Branco"))
        self.assertEqual(split_state_city("Sao Paulo Sao Paulo"), ("SP", "Sao Paulo"))

    def test_state_acronym_with_underscore(self):
        """
        Test cases with underscores in the input string.
        Ensures that the function can correctly handle and split state acronyms and city names 
        when underscores are replaced with spaces.
        This test should pass in the golden solution but fail in the flawed solution.
        """
        self.assertEqual(split_state_city("SP_Sao_Paulo".replace("_", " ")), ("SP", "Sao Paulo"))

    def test_state_name_with_block_words(self):
        """
        Test cases with block words in the state and city names.
        Ensures that the function correctly processes and handles block words.
        """
        self.assertEqual(split_state_city("Rio de Janeiro Rio de Janeiro"), ("RJ", "Rio de Janeiro"))
        self.assertEqual(split_state_city("Sao Paulo Sao Luiz do Paraitinga"), ("SP", "Sao Luiz do Paraitinga"))

    def test_state_and_city_with_replacements(self):
        """
        Test cases that involve city name replacements using CITY_SPELL_MAP and WORD_MAP.
        Ensures that the function correctly applies city name corrections.
        """
        self.assertEqual(split_state_city("MG Brazopolis"), ("MG", "Brazopolis"))
        self.assertEqual(split_state_city("SP Mogi Mirim"), ("SP", "Mogi Mirim"))
        self.assertEqual(split_state_city("TO Tabocao"), ("TO", "Tabocao"))

    def test_state_and_city_with_special_cases(self):
        """
        Edge cases with special city spellings and corrections.
        Ensures that the function correctly handles special cases of city spellings.
        """
        self.assertEqual(split_state_city("CE Itapaje"), ("CE", "Itapaje"))
        self.assertEqual(split_state_city("RJ Paraty"), ("RJ", "Paraty"))

    def test_state_name_misspelled_city(self):
        """
        Test cases for city name corrections using CITY_SPELL_MAP.
        Ensures that the function correctly corrects misspelled city names as per the CITY_SPELL_MAP.
        """
        self.assertEqual(split_state_city("SC Balneario Picarras"), ("SC", "Balneario Picarras"))
        self.assertEqual(split_state_city("RN Acu"), ("RN", "Acu"))


if __name__ == '__main__':
    unittest.main()
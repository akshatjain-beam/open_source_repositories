import unittest
from autuacoes.cities import split_state_city  # Adjust the import based on your module structure

class TestSplitStateCityAdditional(unittest.TestCase):

    def test_state_acronym_rj(self):
        """
        Test case for the state acronym 'RJ'.
        """
        self.assertEqual(split_state_city("RJ Rio de Janeiro"), ("RJ", "Rio de Janeiro"))

    def test_state_acronym_pr(self):
        """
        Test case for the state acronym 'PR'.
        """
        self.assertEqual(split_state_city("PR Curitiba"), ("PR", "Curitiba"))

    def test_full_state_name_bahia(self):
        """
        Test case for the full state name 'Bahia'.
        """
        self.assertEqual(split_state_city("Bahia Salvador"), ("BA", "Salvador"))

    def test_full_state_name_sao_paulo(self):
        """
        Test case for the full state name 'Sao Paulo'.
        """
        self.assertEqual(split_state_city("Sao Paulo Sao Paulo"), ("SP", "Sao Paulo"))

    def test_full_state_name_rio_grande_do_sul(self):
        """
        Test case for the full state name 'Rio Grande do Sul'.
        """
        self.assertEqual(split_state_city("Rio Grande do Sul Porto Alegre"), ("RS", "Porto Alegre"))

if __name__ == '__main__':
    unittest.main()

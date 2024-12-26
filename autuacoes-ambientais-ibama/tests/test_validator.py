import unittest
from autuacoes.validators import cnpj_checks

class TestCnpjChecks(unittest.TestCase):
    """
    Unit test class for testing the cnpj_checks function.
    """

    def test_valid_cnpj(self):
        """
        Test with a valid CNPJ number.
        The expected check digits for the CNPJ '123456789012' should be '30'.
        """
        text = "123456789012"
        expected_result = "30"
        self.assertEqual(cnpj_checks(text), expected_result)

    def test_another_valid_cnpj(self):
        """
        Test with another valid CNPJ number.
        The expected check digits for the CNPJ '987654321098' should be '74'.
        """
        text = "987654321098"
        expected_result = "74"
        self.assertEqual(cnpj_checks(text), expected_result)

    def test_valid_cnpj_3(self):
        """
        Test with another valid CNPJ number.
        The expected check digits for the CNPJ '542118450001' should be '55'.
        """
        text = "542118450001"
        expected_result = "55"
        self.assertEqual(cnpj_checks(text), expected_result)

    def test_valid_cnpj_4(self):
        """
        Test with another valid CNPJ number.
        The expected check digits for the CNPJ '351143090001' should be '97'.
        """
        text = "351143090001"
        expected_result = "97"
        self.assertEqual(cnpj_checks(text), expected_result)

    def test_edge_case_cnpj(self):
        """
        Test with an edge case CNPJ number (all zeros).
        The expected check digits for the CNPJ '000000000000' should be '00'.
        """
        text = "000000000000"
        expected_result = "00"
        self.assertEqual(cnpj_checks(text), expected_result)

    def test_edge_case_cnpj_2(self):
        """
        Test with another edge case CNPJ number (all nines).
        The expected check digits for the CNPJ '999999999999' should be '62'.
        """
        text = "999999999999"
        expected_result = "62"
        self.assertEqual(cnpj_checks(text), expected_result)

if __name__ == "__main__":
    unittest.main()

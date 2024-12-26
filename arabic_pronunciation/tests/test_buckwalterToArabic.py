from arabic_pronunciation.buckwalterToArabic import ArabicScript
import unittest

class TestArabicScriptDictionary(unittest.TestCase):
    """Unit tests for the ArabicScript dictionary mapping from Buckwalter to Arabic script."""

    def setUp(self):
        """Set up the ArabicScript dictionary for testing."""
        self.arabic_script = ArabicScript

    def test_positive_single_character(self):
        """Test if a single Buckwalter character correctly maps to its Arabic script equivalent."""
        self.assertEqual(self.arabic_script['a'], '\u064e')

    def test_positive_special_character(self):
        """Test if a special Buckwalter character correctly maps to its Arabic script equivalent."""
        self.assertEqual(self.arabic_script['*'], '\u0630')

    def test_negative_non_existent_character(self):
        """Test that a non-existent Buckwalter character raises a KeyError."""
        with self.assertRaises(KeyError):
            self.arabic_script['R']

    def test_negative_invalid_character(self):
        """Test that an invalid Buckwalter character raises a KeyError."""
        with self.assertRaises(KeyError):
            self.arabic_script['!']

    def test_edge_case_empty_string(self):
        """Test that an empty string returns None when queried in the dictionary."""
        self.assertIsNone(self.arabic_script.get(""))

if __name__ == '__main__':
    unittest.main()

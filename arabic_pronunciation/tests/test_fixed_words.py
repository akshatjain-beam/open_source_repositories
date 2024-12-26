import unittest
import re
from arabic_pronunciation.fixed_words import isFixedWord2 

class TestIsFixedWord2(unittest.TestCase):
    
    def test_single_pronunciation(self):
        """Test that the function correctly identifies the pronunciation of 'Th'."""
        self.assertEqual(isFixedWord2(u'Th'), [['T', 'aa', 'h', 'a']])
        
    def test_ambiguous_last_letter_a(self):
        """Test that the function returns the correct pronunciation for 'h*A'."""
        self.assertEqual(isFixedWord2(u'h*A'), [['h', 'aa', '*', 'aa']])

    def test_unambiguous_consonant(self):
        """Test that the function correctly handles the unambiguous consonant 'lkn'."""
        self.assertEqual(isFixedWord2(u'lkn'), [['l', 'aa', 'k', 'i1', 'n']])

    def test_last_letter_u(self):
        """Test that the function correctly handles words ending with 'h' and returns the right pronunciation."""
        self.assertEqual(isFixedWord2(u'lknh'), [['l', 'aa', 'k', 'i0', 'nn', 'a', 'h', 'u0']])

    def test_no_match_in_fixed_words(self):
        """Test that the function returns an empty list for words not present in fixedWords."""
        self.assertEqual(isFixedWord2(u'unknown'), [])

    def test_special_case(self):
        """Test that the function correctly identifies the pronunciation of 'lknkmA'."""
        self.assertEqual(isFixedWord2(u'lknkmA'), [['l', 'aa', 'k', 'i0', 'nn', 'a', 'k', 'u0', 'm', 'aa']])

    def test_with_unambiguous_map(self):
        """Test that the function correctly handles unambiguous mappings for '*lk'."""
        self.assertEqual(isFixedWord2(u'*lk'), [['*', 'aa', 'l', 'i0', 'k']])

    def test_list_in_ambiguous_map(self):
        """Test that the function correctly identifies the pronunciation of 'Aw'."""
        self.assertEqual(isFixedWord2(u'Aw'), [['<', 'a', 'w']])

    def test_last_letter_ends_with_a(self):
        """Test case where the last letter is 'a' and should match multiple pronunciations for 'h*A'."""
        expected = [['h', 'aa', '*', 'aa']]
        self.assertEqual(isFixedWord2(u'h*A'), expected)

    def test_last_letter_ends_with_h(self):
        """Test case where the last letter is 'h' should match specific pronunciations for 'lknh'."""
        expected = [['l', 'aa', 'k', 'i0', 'nn', 'a', 'h', 'u0']]
        self.assertEqual(isFixedWord2(u'lknh'), expected) 

if __name__ == '__main__':
    unittest.main()

import unittest
from arabic_pronunciation.arabic_utils import keep_only_arabic

from alphabet_detector import AlphabetDetector


class TestKeepOnlyArabic(unittest.TestCase):
    def setUp(self):
        self.ad = AlphabetDetector()

    def test_keep_only_arabic_positive(self):
        """
        Test with lines containing both Arabic and English words.
        
        This test checks that the function correctly retains Arabic words 
        while discarding English words. The expected output should only 
        include Arabic words from the input text, formatted into lines 
        that correspond to the input structure.
        """
        input_text = "Hello مرحبا\nThis is a test اختبار"
        expected_output = "مرحبا\nاختبار"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_negative(self):
        """
        Test with lines containing only non-Arabic words.
        
        This test verifies that when the input text consists solely of 
        non-Arabic words, the function should return an empty line for 
        each line in the input, indicating no Arabic content was found.
        """
        input_text = "Hello World\nGoodbye"
        expected_output = "\n"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_edge_case_empty(self):
        """
        Test with an empty input string.
        
        This test checks the behavior of the function when no input 
        is provided. The expected output should also be an empty string 
        as there is no content to process.
        """
        input_text = ""
        expected_output = ""
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_edge_case_spaces(self):
        """
        Test with lines that contain only spaces.
        
        This test evaluates how the function handles lines that are 
        composed solely of whitespace. The expected output should be 
        empty lines for each input line, signifying that there is no 
        Arabic content to retain.
        """
        input_text = "     \n   \n"
        expected_output = "\n"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_mixed_words(self):
        """
        Test with lines that contain Arabic and non-Arabic words.
        
        This test checks that the function successfully extracts 
        Arabic phrases from a mix of Arabic and English text. The 
        expected output should only include the Arabic words that 
        are present in the input text.
        """
        input_text = "This is a line with كلمات عربية\nAnd some more كلمات"
        expected_output = "كلمات عربية\nكلمات"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_non_alpha(self):
        """
        Test with Arabic words that include non-alphabetic characters.
        
        This test evaluates the function's ability to ignore Arabic 
        words that are not purely alphabetic, such as those containing 
        digits or punctuation. The expected output should include only 
        the valid Arabic words.
        """
        input_text = "Hello 123 مرحبا!\nاختبار"
        expected_output = "\nاختبار"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_mixed_lines(self):
        """
        Test with a mix of Arabic and English in the same line.
        
        This test checks if the function can extract Arabic words 
        from a line that contains both Arabic and English words. 
        The expected output should include only the Arabic words, 
        excluding any English content.
        """
        input_text = "This line has some عربى words and some English"
        expected_output = "عربى"
        self.assertEqual(keep_only_arabic(input_text), expected_output)

    def test_keep_only_arabic_special_chars(self):
        """
        Test with special characters mixed with Arabic.
        
        This test verifies that the function can handle special 
        characters alongside Arabic words and correctly retains 
        the Arabic content. The expected output should exclude 
        any special characters.
        """
        input_text = "مرحبا @#$%^&*() اختبار"
        expected_output = "مرحبا اختبار"
        self.assertEqual(keep_only_arabic(input_text), expected_output)


if __name__ == "__main__":
    unittest.main()

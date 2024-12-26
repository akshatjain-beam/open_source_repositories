from arabic_pronunciation.arabic_utils import remove_links
import unittest
import re


class TestRemoveLinks(unittest.TestCase):
    """Unit tests for the remove_links function in the arabic_utils module."""

    def test_no_http_link(self):
        """Test when the text contains a link without http or https, e.g., '://example.com'.
        The function should remove the link and leave the text intact."""
        text = "I want ://example.com"
        self.assertEqual(remove_links(text), "I want ")

    def test_simple_http_link(self):
        """Test a simple HTTP link, e.g., 'http://example.com'.
        The function should remove the link and leave the preceding text intact."""
        text = "I want http://example.com"
        self.assertEqual(remove_links(text), "I want ")
    
    def test_mixed_content(self):
        """Test text with no links at all.
        The function should return the original text unchanged."""
        text = "This is just a simple text without links."
        self.assertEqual(remove_links(text), "This is just a simple text without links.")

    def test_special(self):
        """Test a text that includes a URL with special characters, e.g., 'über'.
        The function should remove the link while preserving the surrounding text."""
        text = "Visit https://example.com/über for more information."
        self.assertEqual(remove_links(text), "Visit  for more information.")
    
    def test_punctuation(self):
        """Test a sentence that includes a URL followed by punctuation, e.g., a comma.
        The function should remove the link and keep the punctuation intact."""
        text = "Check out https://example.com, it's a great resource." 
        self.assertEqual(remove_links(text), "Check out , it's a great resource.")


if __name__ == '__main__':
    unittest.main()

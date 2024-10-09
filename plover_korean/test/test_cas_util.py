"""Unit tests for utility functions."""

import operator
import unittest
import pytest

from plover_korean.system.cas.util import (
    compare_numeric_text,
    get_stroke_groups,
    STROKE_REGEX
)

class TestStrokeRegex(unittest.TestCase):
    """
    Test cases for STROKE_REGEX pattern matching.
    """

    def test_full_match(self):
        """
        Test that a full match with all components present is correctly captured.
        """
        match = STROKE_REGEX.match("3ㅎㅏ7ㄹ")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number_start'), '3')
        self.assertEqual(match.group('initial'), 'ㅎ')
        self.assertEqual(match.group('medial'), 'ㅏ')
        self.assertEqual(match.group('number_end'), '7')
        self.assertEqual(match.group('final'), 'ㄹ')

    def test_empty_string(self):
        """
        Test that an empty string matches, with all groups returning empty strings.
        """
        match = STROKE_REGEX.match("")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number_start'), '')
        self.assertEqual(match.group('initial'), '')
        self.assertEqual(match.group('medial'), '')
        self.assertEqual(match.group('number_end'), '')
        self.assertEqual(match.group('final'), '')

    def test_only_initial(self):
        """
        Test that a string with only the 'initial' component is correctly matched.
        """
        match = STROKE_REGEX.match("ㅎ")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number_start'), '')
        self.assertEqual(match.group('initial'), 'ㅎ')
        self.assertEqual(match.group('medial'), '')
        self.assertEqual(match.group('number_end'), '')
        self.assertEqual(match.group('final'), '')

    def test_invalid_character(self):
        """
        Test that a string with an invalid character does not match.
        """
        match = STROKE_REGEX.match("A")
        self.assertIsNone(match)

    def test_number_start_and_end(self):
        """
        Test that a string with 'number_start', 'medial', 'number_end', and 'final' components is correctly matched.
        """
        match = STROKE_REGEX.match("5ㅓ9ㅇ")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number_start'), '5')
        self.assertEqual(match.group('initial'), '')
        self.assertEqual(match.group('medial'), 'ㅓ')
        self.assertEqual(match.group('number_end'), '9')
        self.assertEqual(match.group('final'), 'ㅇ')

    def test_medial_with_special_character(self):
        """
        Test that a string with 'initial' and 'medial' components, including special characters (*-), is correctly matched.
        """
        match = STROKE_REGEX.match("ㅎ*-")
        self.assertIsNotNone(match)
        self.assertEqual(match.group('number_start'), '')
        self.assertEqual(match.group('initial'), 'ㅎ')
        self.assertEqual(match.group('medial'), '*-')
        self.assertEqual(match.group('number_end'), '')
        self.assertEqual(match.group('final'), '')

if __name__ == '__main__':
    unittest.main()


class TestCompareNumericText(object):
    pass


class TestGetStrokeGroups(object):
    pass
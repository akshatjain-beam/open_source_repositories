import pytest
from datetime import datetime, timedelta, timezone

from usepy import useDateTime


def test_parse():
    assert useDateTime.parse('2020-01-01 00:00:00') == datetime(2020, 1, 1, 0, 0)


def test_format():
    assert useDateTime.format(datetime(2022, 2, 1, 0, 0)) == '2022-02-01 00:00:00'
    assert useDateTime.format(datetime(2022, 2, 1, 0, 0), fmt='%Y-%m-%d') == '2022-02-01'
    assert useDateTime.format_before(1, useDateTime.DAYS) == useDateTime.format(datetime.now() - timedelta(days=1))
    assert useDateTime.format_after(3, useDateTime.HOURS) == useDateTime.format(datetime.now() + timedelta(hours=3))


def test_timestamp():
    assert useDateTime.timestamp(datetime(2022, 2, 1, 0, 0, 0, tzinfo=timezone.utc)) == 1643673600


def test_format_now():
    assert useDateTime.format_now() == useDateTime.format(datetime.now())
    assert useDateTime.format_now(fmt="%Y-%m-%d") == useDateTime.format(datetime.now(), "%Y-%m-%d")

class TestDateTimeParser:
    def test_parse_valid_datetime(self):
        """
        Test parsing a valid datetime string with a specific format.
        
        This test verifies that the `parse` method correctly interprets 
        the datetime string '2024-09-26 14:30:00' when the format 
        '%Y-%m-%d %H:%M:%S' is explicitly provided. The expected result 
        is a datetime object corresponding to September 26, 2024, at 
        14:30 (2:30 PM).
        """
        result = useDateTime.parse('2024-09-26 14:30:00', fmt="%Y-%m-%d %H:%M:%S")
        assert result == datetime(2024, 9, 26, 14, 30)

    def test_parse_valid_date_without_format(self):
        """
        Test parsing a valid date string without providing a format.
        
        This test checks that the `parse` method can correctly parse 
        the date string '01/01/2020' without an explicit format. The 
        expected outcome is a datetime object representing January 1, 
        2020, at 00:00 (midnight).
        """
        result = useDateTime.parse('01/01/2020')
        assert result == datetime(2020, 1, 1, 0, 0)

    def test_parse_valid_date_with_format(self):
        """
        Test parsing a valid date string with a specific format.
        
        This test ensures that the `parse` method correctly parses the 
        date string '09-26-2024' when provided with the format 
        '%m-%d-%Y'. The expected result is a datetime object for 
        September 26, 2024.
        """
        result = useDateTime.parse('09-26-2024', fmt="%m-%d-%Y")
        assert result == datetime(2024, 9, 26)

    def test_parse_invalid_date(self):
        """
        Test parsing an invalid date string.
        
        This test checks the behavior of the `parse` method when 
        attempting to parse an invalid date string 'invalid-date-string'.
        It expects the method to raise a ValueError, indicating that 
        the string does not correspond to a valid date format.
        """
        with pytest.raises(ValueError):
            useDateTime.parse('invalid-date-string')

    def test_parse_empty_string(self):
        """
        Test parsing an empty string.
        
        This test verifies that passing an empty string to the `parse` 
        method raises a ValueError. An empty string does not provide 
        any date information to parse.
        """
        with pytest.raises(ValueError):
            useDateTime.parse('')

    def test_parse_no_format_and_no_valid_format(self):
        """
        Test parsing a valid string that does not match any predefined formats.
        
        This test checks the `parse` method's response to a random 
        string 'random-string' that does not correspond to any date 
        format in the available format lists. It expects a ValueError 
        to be raised.
        """
        with pytest.raises(ValueError):
            useDateTime.parse('random-string')

    def test_parse_edge_case_datetime(self):
        """
        Test edge case parsing of datetime at the boundaries.
        
        This test verifies that the `parse` method correctly handles 
        leap years by parsing '2024-02-29 12:00:00', which should return 
        a datetime object for February 29, 2024, at 12:00 PM. It also 
        checks another edge case with '2023-12-31 23:59:59' to ensure 
        that the last second of the year is parsed correctly.
        """
        result = useDateTime.parse('2024-02-29 12:00:00')  # Leap year
        assert result == datetime(2024, 2, 29, 12, 0)

        result = useDateTime.parse('2023-12-31 23:59:59')
        assert result == datetime(2023, 12, 31, 23, 59, 59)

    def test_parse_with_extra_spaces(self):
        """
        Test parsing a date string with extra spaces.
        
        This test checks that the `parse` method can handle leading 
        and trailing spaces in the date string '   2024-09-26   '. 
        It verifies that the method correctly trims the spaces and 
        returns a datetime object for September 26, 2024.
        """
        result = useDateTime.parse('   2024-09-26   ')
        assert result == datetime(2024, 9, 26)

    def test_parse_invalid_format_provided(self):
        """
        Test passing an incorrect format string that doesn't match the input.
        
        This test checks that when an incorrect format string 
        '%d/%m/%Y' is provided for the date '2024-09-26', the `parse` 
        method raises a ValueError. The input date format does not 
        match the specified format.
        """
        with pytest.raises(ValueError):
            useDateTime.parse('2024-09-26', fmt="%d/%m/%Y")

    def test_parse_partial_date(self):
        """
        Test parsing a partial date string.
        
        This test verifies that the `parse` method raises a ValueError 
        when attempting to parse a partial date string '2024-09'. 
        A complete date must be provided for successful parsing.
        """
        with pytest.raises(ValueError):
            useDateTime.parse('2024-09')  # Invalid as it doesn't represent a full date

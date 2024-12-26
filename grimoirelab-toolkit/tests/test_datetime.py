#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2020 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Santiago Dueñas <sduenas@bitergia.com>
#     Valerio Cosentino <valcos@bitergia.com>
#     Miguel Ángel Fernández <mafesan@bitergia.com>
#     Jesus M. Gonzalez-Barahona <jgb@gsyc.es>
#

import datetime
import unittest

import types
import sys

import dateutil.tz
import dateutil.parser
import dateutil

from grimoirelab_toolkit.datetime import (InvalidDateError,
                                          datetime_to_utc,
                                          str_to_datetime,
                                          unixtime_to_datetime,
                                          datetime_utcnow)


def freeVar(val):
  def nested():
    return val
  return nested.__closure__[0]

codeAttribute = '__code__' if sys.version_info[0] == 3 else 'func_code'

def nested(outer, innerName, **freeVars):
  if isinstance(outer, (types.FunctionType, types.MethodType)):
    outer = outer.__getattribute__(codeAttribute)
  for const in outer.co_consts:
    if isinstance(const, types.CodeType) and const.co_name == innerName:
      return types.FunctionType(const, globals(), None, None, tuple(
          freeVar(freeVars[name]) for name in const.co_freevars))


class TestInvalidDateError(unittest.TestCase):

    def test_message(self):
        """Make sure that prints the correct error"""

        e = InvalidDateError(date='1900-13-01')
        self.assertEqual('1900-13-01 is not a valid date',
                         str(e))


class TestDatetimeToUTC(unittest.TestCase):
    """Unit tests for datetime_to_utc function."""

    def test_conversion(self):
        """Check if it converts some timestamps to timestamps with UTC+0."""

        date = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                 tzinfo=dateutil.tz.tzoffset(None, -21600))
        expected = datetime.datetime(2001, 12, 2, 5, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        utc = datetime_to_utc(date)
        self.assertIsInstance(utc, datetime.datetime)
        self.assertEqual(utc, expected)

        date = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                 tzinfo=dateutil.tz.tzutc())
        expected = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        utc = datetime_to_utc(date)
        self.assertIsInstance(utc, datetime.datetime)
        self.assertEqual(utc, expected)

        date = datetime.datetime(2001, 12, 1, 23, 15, 32)
        expected = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        utc = datetime_to_utc(date)
        self.assertIsInstance(utc, datetime.datetime)
        self.assertEqual(utc, expected)

    def test_invalid_timezone(self):
        """ Check whether datetime converts to UTC when timezone invalid """

        date = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                 tzinfo=dateutil.tz.tzoffset(None, 3600*23))
        expected = datetime.datetime(2001, 12, 1, 0, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        utc = datetime_to_utc(date)
        self.assertIsInstance(utc, datetime.datetime)
        self.assertEqual(utc, expected)

    def test_invalid_datetime(self):
        """Check if it raises an exception on invalid instances."""

        self.assertRaises(InvalidDateError, datetime_to_utc, "2016-01-01 01:00:00 +0800")
        self.assertRaises(InvalidDateError, datetime_to_utc, None)
        self.assertRaises(InvalidDateError, datetime_to_utc, 1)


class TestStrToDatetime(unittest.TestCase):
    """Unit tests for str_to_datetime function."""

    def test_dates(self):
        """
        Check if it converts valid date strings to datetime objects.
        
        This test verifies multiple date formats including:
        - Standard date (YYYY-MM-DD)
        - European date format (DD-MM-YYYY)
        - Two-digit year (YY-MM-DD)
        - Date with time (YYYY-MM-DD HH:MM:SS)
        - Date with various timezone formats including UTC (Z) and offsets (-0600).
        
        The expected outcome is that each date string correctly converts
        to a datetime object with the appropriate timezone information.
        """

        date = str_to_datetime('2001-12-01')
        expected = datetime.datetime(2001, 12, 1, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('13-01-2001')
        expected = datetime.datetime(2001, 1, 13, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('12-01-01')
        expected = datetime.datetime(2001, 12, 1, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('2001-12-01 23:15:32')
        expected = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('2001-12-01 23:15:32 -0600')
        expected = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                     tzinfo=dateutil.tz.tzoffset(None, -21600))
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('2001-12-01 23:15:32Z')
        expected = datetime.datetime(2001, 12, 1, 23, 15, 32,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Wed, 26 Oct 2005 15:20:32 -0100 (GMT+1)')
        expected = datetime.datetime(2005, 10, 26, 15, 20, 32,
                                     tzinfo=dateutil.tz.tzoffset(None, -3600))
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Wed, 22 Jul 2009 11:15:50 +0300 (FLE Daylight Time)')
        expected = datetime.datetime(2009, 7, 22, 11, 15, 50,
                                     tzinfo=dateutil.tz.tzoffset(None, 10800))
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Thu, 14 Aug 2008 02:07:59 +0200 CEST')
        expected = datetime.datetime(2008, 8, 14, 2, 7, 59,
                                     tzinfo=dateutil.tz.tzoffset(None, 7200))
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Tue, 06 Jun 2006 20:50:46 00200 (CEST)')
        expected = datetime.datetime(2006, 6, 6, 20, 50, 46,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Sat, 2 Aug 2008 04:18:59 +0500\x1b[D\x1b[D\x1b[D\x1b[-\x1b[C\x1b[C\x1b[C\x1b[C)')
        expected = datetime.datetime(2008, 8, 2, 4, 18, 59,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Thu, 14 Aug 2008 02:07:59 +0200 +0100')
        expected = datetime.datetime(2008, 8, 14, 2, 7, 59,
                                     tzinfo=dateutil.tz.tzoffset(None, 7200))
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        # This date is invalid because the timezone section.
        # Timezone will be removed, setting UTC as default
        date = str_to_datetime('2001-12-01 02:00 +08888')
        expected = datetime.datetime(2001, 12, 1, 2, 0, 0,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = str_to_datetime('Sun, 28 Feb 1999 19:17:37 -7700 (EST)')
        expected = datetime.datetime(1999, 2, 28, 19, 17, 37,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

    def test_invalid_unixtime_to_datetime(self):
        """
        Check whether it fails with an invalid unixtime.
        
        This test verifies that the `str_to_datetime` function raises an
        `InvalidDateError` when an invalid unixtime string is provided.
        The specific input tested is '2017-07-24', which is not a valid
        unixtime format. The expectation is that the error is raised.
        """

        self.assertRaises(InvalidDateError, unixtime_to_datetime, '2017-07-24')

    def test_invalid_date(self):
        """
        Check whether it fails with invalid date strings.
        
        This test verifies that the `str_to_datetime` function raises an
        `InvalidDateError` when provided with invalid date strings, such
        as '2001-13-01' (invalid month) and '2001-04-31' (invalid day).
        The expectation is that the appropriate error is raised in both cases.
        """

        self.assertRaises(InvalidDateError, str_to_datetime, '2001-13-01')
        self.assertRaises(InvalidDateError, str_to_datetime, '2001-04-31')

    def test_invalid_format(self):
        """
        Check whether it fails with invalid date formats.
        
        This test verifies that the `str_to_datetime` function raises an
        `InvalidDateError` when provided with invalid date format strings,
        such as '2001-12-01mm', 'nodate', or None. The expectation is
        that the function raises the appropriate error for each invalid
        input.
        """

        self.assertRaises(InvalidDateError, str_to_datetime, '2001-12-01mm')
        self.assertRaises(InvalidDateError, str_to_datetime, 'nodate')
        self.assertRaises(InvalidDateError, str_to_datetime, None)
        self.assertRaises(InvalidDateError, str_to_datetime, '')

    def test_datetime_utcnow(self):
        """
        Check whether timezone information is added to the current time.
        
        This test checks that the `datetime_utcnow` function returns the
        current time with the correct timezone information set to UTC.
        The expected timezone format is "UTC+00:00". The test ensures that
        the timezone returned matches this expectation.
        """

        now = datetime_utcnow()
        timezone = str(now.tzinfo)
        expected = "UTC+00:00"

        self.assertTrue(timezone, expected)
    
    def test_iso_format_with_timezone(self):
        """
        Test ISO 8601 format with timezone.
        
        This test checks the `str_to_datetime` function with an ISO 8601
        formatted date string that includes a timezone ('2024-09-18T14:23:45Z').
        The expected output is a datetime object that matches the specified
        date and time in UTC. The expectation is that the conversion is
        performed accurately and the resulting datetime matches the expected
        value.
        """
        date = str_to_datetime('2024-09-18T14:23:45Z')
        expected = datetime.datetime(2024, 9, 18, 14, 23, 45, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)
    
    def test_extreme_future_date(self):
        """
        Test handling of extreme future dates.
        
        This test verifies that the `str_to_datetime` function can correctly
        handle extreme future dates, such as '3000-01-01T00:00:00Z'. The
        expected output is a datetime object corresponding to this date and
        time in UTC. The expectation is that the conversion is successful,
        and the resulting datetime matches the expected value.
        """
        date = str_to_datetime('3000-01-01T00:00:00Z')
        expected = datetime.datetime(3000, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)
    
    def test_empty_string(self):
        """Test handling of empty string."""
        with self.assertRaises(InvalidDateError):
            str_to_datetime('')

    def test_whitespace_string(self):
        """Test handling of whitespace string."""
        with self.assertRaises(InvalidDateError):
            str_to_datetime('    ')


# Helper function for testing the nested function
def helper_nested_parse_datetime(ts):
    nested_parse_datetime = nested(str_to_datetime, 'parse_datetime', ts=ts)
    result = nested_parse_datetime(ts)
    return result


class TestParseDatetime(unittest.TestCase):
    def assert_datetime_equal(self, dt1, dt2):
        """Helper method to assert that two datetime objects are equal by comparing their individual components."""
        self.assertEqual(dt1.year, dt2.year)
        self.assertEqual(dt1.month, dt2.month)
        self.assertEqual(dt1.day, dt2.day)
        self.assertEqual(dt1.hour, dt2.hour)
        self.assertEqual(dt1.minute, dt2.minute)
        self.assertEqual(dt1.second, dt2.second)
        self.assertEqual(dt1.tzinfo, dt2.tzinfo)

    def test_parse_datetime_with_timezone(self):
        """
        Test parsing a datetime string with a specified timezone.
        
        The input string '2024-09-18T12:00:00+02:00' should be parsed to a 
        datetime object representing September 18, 2024, at 12:00 PM with 
        a timezone offset of +2 hours.
        """
        ts = "2024-09-18T12:00:00+02:00"
        expected_dt = datetime.datetime(2024, 9, 18, 12, 0, 0, tzinfo=dateutil.tz.tzoffset(None, 7200))
        result = helper_nested_parse_datetime(ts)

        self.assert_datetime_equal(result, expected_dt)
    
    def test_parse_datetime_without_timezone(self):
        """
        Test parsing a datetime string without a timezone.
        
        The input string '2024-09-18T12:00:00' should be parsed to a 
        datetime object representing September 18, 2024, at 12:00 PM in 
        UTC.
        """
        ts = "2024-09-18T12:00:00"
        expected_dt = datetime.datetime(2024, 9, 18, 12, 0, 0, tzinfo=dateutil.tz.tzutc())
        result = helper_nested_parse_datetime(ts)
        
        self.assert_datetime_equal(result, expected_dt)

    def test_parse_datetime_with_utc(self):
        """
        Test parsing a datetime string that uses 'Z' to denote UTC.
        
        The input string '2024-09-18T12:00:00Z' should be parsed to a 
        datetime object representing September 18, 2024, at 12:00 PM in 
        UTC.
        """
        ts = "2024-09-18T12:00:00Z"
        expected_dt = datetime.datetime(2024, 9, 18, 12, 0, 0, tzinfo=dateutil.tz.tzutc())
        result = helper_nested_parse_datetime(ts)
        
        self.assert_datetime_equal(result, expected_dt)

    def test_parse_datetime_with_date_only(self):
        """
        Test parsing a date-only string.
        
        The input string '2024-09-18' should be parsed to a datetime 
        object representing September 18, 2024, at 00:00:00 in UTC.
        """
        ts = "2024-09-18"
        expected_dt = datetime.datetime(2024, 9, 18, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        result = helper_nested_parse_datetime(ts)
        
        self.assert_datetime_equal(result, expected_dt)
    
    def test_parse_datetime_with_ambiguous_date(self):
        """
        Test parsing a datetime string with an ambiguous format.
        
        The input string '2024-09-18T00:00:00+0000' should be parsed to a 
        datetime object representing September 18, 2024, at 00:00:00 in 
        UTC.
        """
        ts = "2024-09-18T00:00:00+0000"
        expected_dt = datetime.datetime(2024, 9, 18, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        result = helper_nested_parse_datetime(ts)
        
        self.assert_datetime_equal(result, expected_dt)
    
    def test_parse_datetime_with_empty_string(self):
        """
        Test parsing an empty string.
        
        An empty string should raise a ValueError, as it is not a valid 
        datetime format.
        """
        ts = ""
        with self.assertRaises(ValueError):
            helper_nested_parse_datetime(ts)

    def test_parse_datetime_with_future_date(self):
        """
        Test parsing a future date.
        
        The input string '3000-01-01T00:00:00Z' should be parsed to a 
        datetime object representing January 1, 3000, at 00:00:00 in 
        UTC.
        """
        ts = "3000-01-01T00:00:00Z"
        expected_dt = datetime.datetime(3000, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        result = helper_nested_parse_datetime(ts)
        
        self.assert_datetime_equal(result, expected_dt)
    def test_invalid_timezone_format(self):
        """
        Test handling of dates with invalid timezone formats.
        
        This test checks that the `str_to_datetime` function can handle dates
        with invalid timezone formats, such as '2024-09-18T14:23:45 +9999'.
        In this case, the function should ignore the invalid timezone and
        default to UTC. The expectation is that the resulting datetime object
        matches the expected value in UTC.
        """
        date = str_to_datetime('2024-09-18T14:23:45 +9999')
        expected = datetime.datetime(2024, 9, 18, 14, 23, 45, tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)
    
    def test_empty_string(self):
        """
        Test handling of empty string input.
        
        This test verifies that the `str_to_datetime` function raises an
        `InvalidDateError` when provided with an empty string as input.
        The expectation is that the function does not accept empty strings
        and raises the appropriate error.
        """
        with self.assertRaises(InvalidDateError):
            str_to_datetime('')

    def test_whitespace_string(self):
        """
        Test handling of strings containing only whitespace.
        
        This test checks that the `str_to_datetime` function raises an
        `InvalidDateError` when provided with a string that consists only
        of whitespace. The expectation is that such inputs are considered
        invalid, and the function raises the appropriate error.
        """
        with self.assertRaises(InvalidDateError):
            str_to_datetime('    ')


class TestUnixTimeToDatetime(unittest.TestCase):
    """Unit tests for str_to_datetime function."""

    def test_dates(self):
        """Check if it converts some timestamps to datetime objects."""

        date = unixtime_to_datetime(0)
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

        date = unixtime_to_datetime(1426868155.0)
        expected = datetime.datetime(2015, 3, 20, 16, 15, 55,
                                     tzinfo=dateutil.tz.tzutc())
        self.assertIsInstance(date, datetime.datetime)
        self.assertEqual(date, expected)

    def test_invalid_format(self):
        """Check whether it fails with invalid formats."""

        self.assertRaises(InvalidDateError, str_to_datetime, '2001-12-01mm')
        self.assertRaises(InvalidDateError, str_to_datetime, 'nodate')
        self.assertRaises(InvalidDateError, str_to_datetime, None)
        self.assertRaises(InvalidDateError, str_to_datetime, '')


if __name__ == "__main__":
    unittest.main(warnings='ignore')

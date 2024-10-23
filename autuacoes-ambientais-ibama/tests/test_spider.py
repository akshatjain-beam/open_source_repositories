import unittest
from unittest.mock import call, patch
from autuacoes.spider import AutuacoesSpider
import datetime
import tempfile
import os
from urllib.parse import quote


class TestAutuacoesSpider(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for the download path
        self.download_path = tempfile.mkdtemp()
        self.spider = AutuacoesSpider(download_path=self.download_path)

    def tearDown(self):
        # Clean up the temporary directory after tests
        try:
            os.rmdir(self.download_path)  # Remove the temporary directory
        except OSError:
            pass  # If the directory is not empty, ignore the error

    @patch('autuacoes.spider.date_range')
    def test_start_requests_end_date(self, mock_date_range):
        """
        Test that the end date is correctly calculated for requests.

        This test mocks the return value of the date_range function to
        control the years being processed. It verifies that the requests
        generated contain the correct start and end dates in their URLs.
        """
        # Mock the return value of date_range
        mock_date_range.return_value = [datetime.date(
            2020, 1, 1), datetime.date(2021, 1, 1)]

        # Call the start_requests method
        requests = list(self.spider.start_requests())

        # Check that the end_date is correctly calculated
        expected_end_dates = [datetime.date(
            2020, 12, 31), datetime.date(2021, 12, 31)]

        for i, request in enumerate(requests):
            # Create URL-encoded start and end dates
            start_date = quote("01/01/{}".format(expected_end_dates[i].year))
            end_date = quote("31/12/{}".format(expected_end_dates[i].year))

            # Check that the request contains the correct dates in the URL
            self.assertIn(start_date, request.url)
            self.assertIn(end_date, request.url)


TEST_STATE_CODES = {
    "12": "AC",  # Cities from Acre
    "27": "AL",  # Cities from Alagoas
    "13": "AM"   # Cities from Amazonas
}


class TestAutuacoesSpider(unittest.TestCase):
    def setUp(self):
        self.spider = AutuacoesSpider(download_path='test_download')
        self.spider.start_date = datetime.date(2000, 1, 1)
        self.spider.end_date = datetime.date(2000, 12, 31)

    @patch('autuacoes.spider.STATE_CODES', TEST_STATE_CODES)
    @patch.object(AutuacoesSpider, 'make_request')
    def test_start_requests(self, mock_make_request):
        """
        Test the start_requests method when make_request returns None.

        This test verifies that no requests are yielded when all
        state codes lead to None from the make_request mock.
        It also checks that make_request is called with the correct
        parameters for each state code.
        """
        # Mock make_request to return None
        mock_make_request.return_value = None

        # Call start_requests
        requests = list(self.spider.start_requests())

        # Ensure make_request was called with the correct parameters
        expected_calls = [
            ('12', datetime.date(2000, 1, 1), datetime.date(2000, 12, 31)),
            ('27', datetime.date(2000, 1, 1), datetime.date(2000, 12, 31)),
            ('13', datetime.date(2000, 1, 1), datetime.date(2000, 12, 31)),
            ('12', datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)),
            ('27', datetime.date(2001, 1, 1), datetime.date(2001, 12, 31)),
            ('13', datetime.date(2001, 1, 1), datetime.date(2001, 12, 31))
        ]

        # Check that make_request was called for each state code
        calls = [call[0] for call in mock_make_request.call_args_list]

        for got, expect in zip(calls, expected_calls):
            self.assertEqual(got, expect)

        # Ensure no requests were yielded since make_request returns None
        self.assertEqual(requests, [])

    @patch('autuacoes.spider.STATE_CODES', TEST_STATE_CODES)
    @patch.object(AutuacoesSpider, 'make_request')
    def test_start_requests_mixed_requests(self, mock_make_request):
        """
        Test start_requests with mixed return values from make_request.

        This test mocks make_request to return valid requests for some
        state codes and None for others. It verifies that the requests
        yielded match the expected requests based on the mock's behavior.
        """
        # Mock make_request to return valid requests for some codes and None for others
        def side_effect(code, date, end_date):
            return f'request_{code}_{date}_{end_date}' if code != '12' else None

        mock_make_request.side_effect = side_effect

        # Call start_requests
        requests = list(self.spider.start_requests())

        # Prepare expected requests based on the mock's behavior for the years 2000 and 2001
        expected_requests = []
        for year in range(2000, 2002):  # Spanning two years
            for code in TEST_STATE_CODES.keys():
                if code != '12':  # Exclude '12' which returns None
                    expected_requests.append(
                        f'request_{code}_{datetime.date(year, 1, 1)}_{datetime.date(year, 12, 31)}')

        print(requests)
        print(expected_requests)

        # Check that the yielded requests match the expected values
        self.assertEqual(requests, expected_requests)

    @patch('autuacoes.spider.STATE_CODES', TEST_STATE_CODES)
    @patch.object(AutuacoesSpider, 'make_request')
    def test_start_requests_empty_date_range(self, mock_make_request):
        """
        Test start_requests when the date range is minimal (same start and end date).

        This test sets the start and end date to the same value, simulating
        a minimal date range. It verifies that no requests are yielded
        since the range does not cover any full dates.
        """
        # Set an empty date range
        self.spider.start_date = datetime.date(2000, 1, 1)
        self.spider.end_date = datetime.date(2000, 1, 1)

        # Mock make_request to return None
        mock_make_request.return_value = None

        # Call start_requests
        requests = list(self.spider.start_requests())

        # Ensure no requests are yielded since the date range is minimal
        self.assertEqual(requests, [])

    @patch('autuacoes.spider.STATE_CODES', {})
    @patch.object(AutuacoesSpider, 'make_request')
    def test_start_requests_empty_state_codes(self, mock_make_request):
        """
        Test start_requests when STATE_CODES is empty.

        This test verifies that no requests are yielded when the STATE_CODES
        dictionary is empty, simulating a scenario where no state codes are available.
        """
        # Mock make_request to return None
        mock_make_request.return_value = None

        # Call start_requests
        requests = list(self.spider.start_requests())

        # Ensure no requests are yielded since STATE_CODES is empty
        self.assertEqual(requests, [])

    @patch('autuacoes.spider.STATE_CODES', TEST_STATE_CODES)
    @patch.object(AutuacoesSpider, 'make_request')
    def test_start_requests_multiple_years(self, mock_make_request):
        """
        Test start_requests across multiple years.

        This test verifies that the requests generated for multiple years
        call make_request with the correct parameters for each state code.
        It also checks that the correct number of valid requests are yielded.
        """
        # Mock make_request to return valid requests
        mock_make_request.side_effect = lambda code, date, end_date: call(
            code, date, end_date)

        # Call start_requests
        requests = list(self.spider.start_requests())

        # Prepare expected calls for each state code for the years 2000 and 2001
        expected_calls = [
            call(code, datetime.date(year, 1, 1), datetime.date(year, 12, 31))
            for year in range(2000, 2002)  # Spanning two years
            for code in TEST_STATE_CODES.keys()
        ]

        # Check that make_request was called for each state code for both years
        mock_make_request.assert_has_calls(expected_calls, any_order=True)

        # Check that valid requests are yielded
        self.assertEqual(len(requests), len(expected_calls))


if __name__ == '__main__':
    unittest.main()

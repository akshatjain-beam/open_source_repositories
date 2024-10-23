import unittest
from unittest.mock import patch, MagicMock
from autuacoes.spider import AutuacoesSpider  # Adjust the import based on your module structure
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
        # Mock the return value of date_range
        mock_date_range.return_value = [datetime.date(2020, 1, 1), datetime.date(2021, 1, 1)]

        # Call the start_requests method
        requests = list(self.spider.start_requests())

        # Check that the end_date is correctly calculated
        expected_end_dates = [datetime.date(2020, 12, 31), datetime.date(2021, 12, 31)]
        
        for i, request in enumerate(requests):
            # Create URL-encoded start and end dates
            start_date = quote("01/01/{}".format(expected_end_dates[i].year))
            end_date = quote("31/12/{}".format(expected_end_dates[i].year))

            # Check that the request contains the correct dates in the URL
            self.assertIn(start_date, request.url)
            self.assertIn(end_date, request.url)

if __name__ == '__main__':
    unittest.main()
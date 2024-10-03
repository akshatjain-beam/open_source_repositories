import unittest
from urllib.parse import urlparse
from src.emr_cli.packaging.python_poetry_project import PythonPoetryProject  # Replace with the actual class name

class TestParseBucketUri(unittest.TestCase):

    def setUp(self):
        self.instance = PythonPoetryProject()  # Replace with your class that contains _parse_bucket_uri

    def test_parse_valid_uri(self):
        uri = 's3://my-bucket/my/prefix'
        expected_output = ['my-bucket', 'my/prefix']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_no_prefix(self):
        uri = 's3://my-bucket/'
        expected_output = ['my-bucket', '']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_leading_slash_in_prefix(self):
        uri = 's3://my-bucket//my/prefix'
        expected_output = ['my-bucket', 'my/prefix']  # Leading slash in prefix should be stripped
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_trailing_slash(self):
        uri = 's3://my-bucket/my/prefix/'
        expected_output = ['my-bucket', 'my/prefix']  # Trailing slash in prefix should be stripped
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_special_chars(self):
        """Test a valid S3 URI with special characters in the bucket name."""
        uri = 's3://my-bucket_123/my/prefix'
        expected_output = ['my-bucket_123', 'my/prefix']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)



if __name__ == '__main__':
    unittest.main()

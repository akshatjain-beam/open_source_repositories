import unittest
from urllib.parse import urlparse
from src.emr_cli.packaging.python_poetry_project import PythonPoetryProject  # Replace with the actual class name

class TestParseBucketUri(unittest.TestCase):
    """Unit tests for the _parse_bucket_uri method in the PythonPoetryProject class.

    This class contains tests that verify the correct behavior of the
    _parse_bucket_uri method when provided with various S3 URI formats.
    """

    def setUp(self):
        """Initialize a PythonPoetryProject instance for testing."""
        self.instance = PythonPoetryProject()  # Replace with your class that contains _parse_bucket_uri

    def test_parse_valid_uri(self):
        """Test a valid S3 URI with both bucket name and prefix.

        Verifies that the method correctly extracts the bucket name
        and the prefix from a well-formed S3 URI.
        """
        uri = 's3://my-bucket/my/prefix'
        expected_output = ['my-bucket', 'my/prefix']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_no_prefix(self):
        """Test an S3 URI that contains a bucket name but no prefix.

        Verifies that when the URI has a bucket name but lacks a prefix,
        the method returns an empty string for the prefix.
        """
        uri = 's3://my-bucket/'
        expected_output = ['my-bucket', '']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_leading_slash_in_prefix(self):
        """Test an S3 URI with a leading slash in the prefix.

        Verifies that the method correctly strips a leading slash from
        the prefix, ensuring the returned prefix is formatted correctly.
        """
        uri = 's3://my-bucket//my/prefix'
        expected_output = ['my-bucket', 'my/prefix']  # Leading slash in prefix should be stripped
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_trailing_slash(self):
        """Test an S3 URI with a trailing slash in the prefix.

        Verifies that the method correctly ignores a trailing slash in
        the prefix, ensuring the returned prefix is formatted correctly.
        """
        uri = 's3://my-bucket/my/prefix/'
        expected_output = ['my-bucket', 'my/prefix']  # Trailing slash in prefix should be stripped
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

    def test_parse_uri_with_special_chars(self):
        """Test a valid S3 URI with special characters in the bucket name.

        Verifies that the method can handle bucket names containing
        special characters and correctly extracts the bucket name and prefix.
        """
        uri = 's3://my-bucket_123/my/prefix'
        expected_output = ['my-bucket_123', 'my/prefix']
        result = self.instance._parse_bucket_uri(uri)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

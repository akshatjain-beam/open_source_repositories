import unittest
from unittest.mock import patch, MagicMock
import boto3
from src.emr_cli.packaging.python_files_project import PythonFilesProject

class TestDeployMethod(unittest.TestCase):
    
    def setUp(self):
        """
        Set up the test case by creating an instance of PythonFilesProject 
        and configuring necessary attributes for the tests.
        """
        # Create an instance of the class that contains the deploy method
        self.instance = PythonFilesProject()
        self.instance.entry_point_path = "local/path/to/entry_point.py"
        self.instance.dist_dir = "local/path/to/dist"

    @patch('boto3.client')
    @patch('src.emr_cli.packaging.python_files_project.console_log')
    @patch('src.emr_cli.packaging.python_files_project.parse_bucket_uri')
    def test_deploy_success(self, mock_parse_bucket_uri, mock_console_log, mock_boto_client):
        """
        Test the successful deployment of code to S3.
        Mocks the S3 client and checks that the entry point and zip file
        are uploaded correctly. Asserts that the correct S3 URI is returned.
        """
        # Arrange
        s3_code_uri = 's3://my-bucket/my/prefix'
        mock_parse_bucket_uri.return_value = ('my-bucket', 'my/prefix')
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        
        # Act
        result = self.instance.deploy(s3_code_uri)

        # Assert
        mock_s3_client.upload_file.assert_any_call('local/path/to/entry_point.py', 'my-bucket', 'my/prefix/entry_point.py')
        mock_s3_client.upload_file.assert_any_call('local/path/to/dist/pyfiles.zip', 'my-bucket', 'my/prefix/pyfiles.zip')
        self.assertEqual(result, 's3://my-bucket/my/prefix/entry_point.py')

    @patch('boto3.client')
    @patch('src.emr_cli.packaging.python_files_project.console_log')
    @patch('src.emr_cli.packaging.python_files_project.parse_bucket_uri')
    def test_deploy_invalid_uri(self, mock_parse_bucket_uri, mock_console_log, mock_boto_client):
        """
        Test deployment with an invalid S3 URI.
        Asserts that an exception is raised when the URI format is invalid.
        """
        # Arrange
        s3_code_uri = 'invalid-uri'
        mock_parse_bucket_uri.side_effect = Exception("Invalid URI format")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.instance.deploy(s3_code_uri)
        self.assertTrue("Invalid URI format" in str(context.exception))

    @patch('boto3.client')
    @patch('src.emr_cli.packaging.python_files_project.console_log')
    @patch('src.emr_cli.packaging.python_files_project.parse_bucket_uri')
    def test_deploy_file_not_found(self, mock_parse_bucket_uri, mock_console_log, mock_boto_client):
        """
        Test deployment when the entry point file is not found.
        Mocks the S3 client to raise a FileNotFoundError during the upload,
        and asserts that the correct exception is raised.
        """
        # Arrange
        s3_code_uri = 's3://my-bucket/my/prefix'
        mock_parse_bucket_uri.return_value = ('my-bucket', 'my/prefix')
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.upload_file.side_effect = FileNotFoundError("File not found")
        
        # Act & Assert
        with self.assertRaises(FileNotFoundError) as context:
            self.instance.deploy(s3_code_uri)
        self.assertTrue("File not found" in str(context.exception))

    @patch('boto3.client')
    @patch('src.emr_cli.packaging.python_files_project.console_log')
    @patch('src.emr_cli.packaging.python_files_project.parse_bucket_uri')
    def test_deploy_s3_upload_error(self, mock_parse_bucket_uri, mock_console_log, mock_boto_client):
        """
        Test deployment when there is an error during the S3 upload process.
        Mocks the S3 client to raise an exception during upload and asserts
        that the exception is properly raised and caught.
        """
        # Arrange
        s3_code_uri = 's3://my-bucket/my/prefix'
        mock_parse_bucket_uri.return_value = ('my-bucket', 'my/prefix')
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.upload_file.side_effect = Exception("S3 upload failed")
        
        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.instance.deploy(s3_code_uri)
        self.assertTrue("S3 upload failed" in str(context.exception))

    @patch('boto3.client')
    @patch('src.emr_cli.packaging.python_files_project.console_log')
    @patch('src.emr_cli.packaging.python_files_project.parse_bucket_uri')
    def test_deploy_zip_file_not_found(self, mock_parse_bucket_uri, mock_console_log, mock_boto_client):
        """
        Test deployment when the zip file is not found.
        Mocks the S3 client to raise a FileNotFoundError specifically for
        the zip upload, and asserts that the exception is raised correctly.
        """
        # Arrange
        s3_code_uri = 's3://my-bucket/my/prefix'
        mock_parse_bucket_uri.return_value = ('my-bucket', 'my/prefix')
        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        # Simulate that the zip file does not exist
        self.instance.entry_point_path = "local/path/to/entry_point.py"  # Ensure the entry point exists
        self.instance.dist_dir = "local/path/to/dist"  # Ensure the dist dir is set correctly
        mock_s3_client.upload_file.side_effect = FileNotFoundError("Zip file not found")  # Simulate error for the zip upload

        # Act & Assert
        with self.assertRaises(FileNotFoundError) as context:
            self.instance.deploy(s3_code_uri)
        self.assertTrue("Zip file not found" in str(context.exception))


if __name__ == '__main__':
    unittest.main()

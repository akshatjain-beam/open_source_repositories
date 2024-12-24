import pytest
import subprocess
from unittest.mock import patch
from todo_txt_gtd import tdtproj
from unittest.mock import patch, MagicMock

def test_default_file_success():
    """
    Test the default_file function with valid output containing the task_path.

    This test mocks the subprocess.run function to return a successful process
    result with stdout containing the "task_path". The test verifies that the
    default_file function correctly extracts and returns the task_path.

    Expectations:
        The returned task_path should be "/home/user/todo.txt".
    """
    # Test with a valid output containing the task_path
    mock_output = "task_path = /home/user/todo.txt\nother_info = value"

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["todo.txt", "--info"],
            returncode=0,
            stdout=mock_output
        )

        result = tdtproj.default_file()
        assert result == "/home/user/todo.txt"
        
        # Check that subprocess.run was called with the correct filename
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "todo.txt" in args

def test_default_file_no_task_path():
    """
    Test the default_file function with output missing the task_path.

    This test mocks the subprocess.run function to return a successful process
    result with stdout that does not contain "task_path". The test verifies that
    the default_file function raises an AttributeError.

    Expectations:
        An AttributeError should be raised with the message indicating that
        'NoneType' object has no attribute 'group'.
    """
    # Test with output missing the task_path
    mock_output = "other_info = value"

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["todo.txt", "--info"],
            returncode=0,
            stdout=mock_output
        )

        with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'group'"):
            tdtproj.default_file()
        
        # Check that subprocess.run was called with the correct filename
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "todo.txt" in args

def test_default_file_empty_output():
    """
    Test the default_file function with empty output from subprocess.

    This test mocks the subprocess.run function to return a successful process
    result with empty stdout. The test verifies that the default_file function
    raises an AttributeError.

    Expectations:
        An AttributeError should be raised with the message indicating that
        'NoneType' object has no attribute 'group'.
    """
    # Test with empty output from subprocess
    mock_output = ""

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["todo.txt", "--info"],
            returncode=0,
            stdout=mock_output
        )

        with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'group'"):
            tdtproj.default_file()
        
        # Check that subprocess.run was called with the correct filename
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "todo.txt" in args

def test_default_file_invalid_format():
    """
    Test the default_file function with output that has an invalid format.

    This test mocks the subprocess.run function to return a successful process
    result with stdout that does not match the expected format for "task_path".
    The test verifies that the default_file function raises an AttributeError.

    Expectations:
        An AttributeError should be raised with the message indicating that
        'NoneType' object has no attribute 'group'.
    """
    # Test with output that has an invalid format
    mock_output = "task_path_not_correct = /home/user/todo.txt"

    with patch('subprocess.run') as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(
            args=["todo.txt", "--info"],
            returncode=0,
            stdout=mock_output
        )

        with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'group'"):
            tdtproj.default_file()
        
        # Check that subprocess.run was called with the correct filename
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "todo.txt" in args

def test_default_file_subprocess_error():
    """
    Test the default_file function with a subprocess error.

    This test mocks the subprocess.run function to raise a CalledProcessError.
    The test verifies that the default_file function raises the same
    CalledProcessError.

    Expectations:
        A CalledProcessError should be raised.
    """
    # Test with a subprocess error
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, ["todo.txt", "--info"])

        with pytest.raises(subprocess.CalledProcessError):
            tdtproj.default_file()
        
        # Check that subprocess.run was called with the correct filename
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "todo.txt" in args

@patch('subprocess.run')
def test_default_file_code1_passes(mock_run):
    """
    Test the `default_file` function

    This test verifies that the function correctly extracts the 
    task path from the output of the subprocess run command. It 
    mocks the `subprocess.run` method to return a specific 
    stdout value simulating the expected output of `todo.sh config`.
    
    The test checks:
    - That the function returns the correct path.
    - That `subprocess.run` is called once and that the command 
      includes 'todo.txt'.
    """
    # Mock the output of the subprocess.run for code 1
    mock_run.return_value = MagicMock(stdout='task_path = /path/to/todo.txt')
    
    result = tdtproj.default_file()
    
    # Check that the correct path is returned
    assert result == '/path/to/todo.txt'
    
    # Check that subprocess.run was called with the correct arguments
    mock_run.assert_called_once()
    args= mock_run.call_args[0][0]
    assert "todo.txt" in args
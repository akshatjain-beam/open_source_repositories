import pytest
import subprocess
from unittest.mock import patch
from todo_txt_gtd import tdtproj

def test_default_file_success():
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

def test_default_file_no_task_path():
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

def test_default_file_empty_output():
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

def test_default_file_invalid_format():
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

def test_default_file_subprocess_error():
    # Test with a subprocess error
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, ["todo.txt", "--info"])

        with pytest.raises(subprocess.CalledProcessError):
            tdtproj.default_file()

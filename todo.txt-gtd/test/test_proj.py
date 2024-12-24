from unittest.mock import patch, MagicMock
from todo_txt_gtd.tdtproj import save_selected_projs
from todo_txt_gtd.tdtcleanup import Project


def mock_read_proj(path):
    return {
        "proj1": MagicMock(),
        "proj2": MagicMock(),
        "proj3": MagicMock()
    }


def mock_write_proj(path, data):
    print(f"Called write_proj with path: {path} and data: {data}")
    pass


def get_expected_data_for_filter_terms():
    return {"proj1": MagicMock()}


def get_expected_data_for_exact_match():
    return {"proj1": MagicMock()}


@patch('todo_txt_gtd.tdtproj.read_proj', side_effect=mock_read_proj)
@patch('todo_txt_gtd.tdtproj.write_proj', side_effect=mock_write_proj)
def test_save_selected_projs_filter_terms(mock_write, mock_read):
    """
    Test the save_selected_projs function with filter terms.

    This test verifies that the function correctly filters projects based on
    provided terms and writes the correct data to the edit path.

    Expectations:
        The correct projects should be written to editpath based on filtering terms.
    """
    tdpath = "mock_tdpath"
    editpath = "mock_editpath"
    terms = ["proj1"]
    exact = False

    result = save_selected_projs(tdpath, editpath, terms, exact)

    expected_data = get_expected_data_for_filter_terms()
    mock_write.assert_called_once()
    call_args = mock_write.call_args[0]
    actual_data = call_args[1]

    assert call_args[0] == editpath
    assert set(expected_data.keys()) == set(actual_data.keys())
    for key in expected_data:
        assert isinstance(actual_data[key], MagicMock)

    assert result == {"proj1"}


@patch('todo_txt_gtd.tdtproj.read_proj', side_effect=mock_read_proj)
@patch('todo_txt_gtd.tdtproj.write_proj', side_effect=mock_write_proj)
def test_save_selected_projs_exact_match(mock_write, mock_read):
    """
    Test the save_selected_projs function with exact match.

    This test verifies that the function correctly finds projects that match
    the provided terms exactly and writes the correct data to the edit path.

    Expectations:
        The correct projects should be written to editpath based on exact match.
    """
    tdpath = "mock_tdpath"
    editpath = "mock_editpath"
    terms = ["proj1"]
    exact = True

    result = save_selected_projs(tdpath, editpath, terms, exact)

    expected_data = get_expected_data_for_exact_match()
    mock_write.assert_called_once()
    call_args = mock_write.call_args[0]
    actual_data = call_args[1]

    assert call_args[0] == editpath
    assert set(expected_data.keys()) == set(actual_data.keys())
    for key in expected_data:
        assert isinstance(actual_data[key], MagicMock)

    assert result == {"proj1"}


@patch('todo_txt_gtd.tdtproj.read_proj', return_value={})
@patch('todo_txt_gtd.tdtproj.write_proj', side_effect=mock_write_proj)
def test_save_selected_projs_add_new_project(mock_write, mock_read):
    """
    Test the save_selected_projs function when adding a new project.

    This test verifies that if there are no matching projects, a new project
    is created and added to the data written to the edit path.

    Expectations:
        A new project should be added to the written data.
    """
    tdpath = "mock_tdpath"
    editpath = "mock_editpath"
    terms = ["new_proj"]
    exact = False

    result = save_selected_projs(tdpath, editpath, terms, exact)

    expected_data = {"new_proj": Project("new_proj")}
    mock_write.assert_called_once()
    call_args = mock_write.call_args[0]
    actual_data = call_args[1]

    assert call_args[0] == editpath
    assert set(expected_data.keys()) == set(actual_data.keys())
    for key in expected_data:
        assert isinstance(actual_data[key], Project)
        assert actual_data[key].name == expected_data[key].name

    assert result == {"new_proj"}


@patch('todo_txt_gtd.tdtproj.read_proj', side_effect=mock_read_proj)
@patch('todo_txt_gtd.tdtproj.write_proj', side_effect=mock_write_proj)
def test_save_selected_projs_empty_terms(mock_write, mock_read):
    """
    Test the save_selected_projs function with empty terms.

    This test verifies that if no terms are provided, all projects are written
    to the edit path.

    Expectations:
        All existing projects should be written to the edit path.
    """
    tdpath = "mock_tdpath"
    editpath = "mock_editpath"
    terms = []
    exact = False

    result = save_selected_projs(tdpath, editpath, terms, exact)

    expected_data = mock_read_proj(tdpath)
    mock_write.assert_called_once()
    call_args = mock_write.call_args[0]
    actual_data = call_args[1]

    assert call_args[0] == editpath
    assert set(expected_data.keys()) == set(actual_data.keys())
    for key in expected_data:
        assert isinstance(actual_data[key], MagicMock)

    assert result == {"proj1", "proj2", "proj3"}


@patch('todo_txt_gtd.tdtproj.read_proj', side_effect=mock_read_proj)
@patch('todo_txt_gtd.tdtproj.write_proj', side_effect=mock_write_proj)
def test_save_selected_projs_empty_list_after_filtering(mock_write, mock_read):
    """
    Test the save_selected_projs function when filtering results in no matches.

    This test verifies that if the filtering terms do not match any existing
    projects, the new project should still be added.

    Expectations:
        The non-existing project should be added to the written data.
    """
    tdpath = "mock_tdpath"
    editpath = "mock_editpath"
    terms = ["non_existing_proj"]
    exact = False

    result = save_selected_projs(tdpath, editpath, terms, exact)

    expected_data = {"non_existing_proj": Project}
    mock_write.assert_called_once()
    call_args = mock_write.call_args[0]
    actual_data = call_args[1]

    assert call_args[0] == editpath
    assert set(expected_data.keys()) == set(actual_data.keys())
    for key in expected_data:
        assert isinstance(actual_data[key], Project)

    assert result == {"non_existing_proj"}
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

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

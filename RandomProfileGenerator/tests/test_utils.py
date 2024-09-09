import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from random_profile.utils import generate_dob_age

class RandintMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calls = []

    def __call__(self, start, end):
        self.calls.append((start, end))
        return super().__call__(start, end)

@pytest.fixture
def mock_datetime():
    with patch('random_profile.utils.datetime') as mock:
        fixed_now = datetime(2024, 9, 6)
        mock_now = MagicMock()
        mock_now.return_value = fixed_now
        mock.now = mock_now

        mock.side_effect = lambda *args, **kw: datetime(*args, **kw)

        yield mock

@pytest.fixture
def mock_randint():
    with patch('random_profile.utils.random.randint', new_callable=RandintMock) as mock:
        yield mock

def test_edge_case_31_day_month(mock_datetime, mock_randint):
    mock_randint.side_effect = [7, 31, 1990]
    
    dob, age = generate_dob_age()

    # Assert the random.randint calls were as expected
    sorted_calls = sorted(mock_randint.call_args_list)
    expected_sorted_calls = [
        ((1, 12),),
        ((1, 31),),
        ((1944, 2006),)
    ]
    assert sorted_calls == expected_sorted_calls


def test_generate_dob_age():
    dob, age = generate_dob_age()

    # Check that dob is a valid date string in the format "dd/mm/yyyy"
    day, month, year = map(int, dob.split('/'))
    datetime(day=day, month=month, year=year)  # will raise ValueError if not a valid date

    # Check that age is an integer
    assert isinstance(age, int)

    # Check that age is within a reasonable range
    current_year = datetime.now().year
    assert current_year - 80 <= int(year) <= current_year - 18

def test_generate_dob_age_february():
    # Run the test multiple times to ensure February dates are handled correctly
    for _ in range(100):
        dob, age = generate_dob_age()
        day, month, year = map(int, dob.split('/'))
        if month == 2:
            assert 1 <= day <= 28

def test_generate_dob_age_30_days():
    # Run the test multiple times to ensure 30-day months are handled correctly
    for _ in range(100):
        dob, age = generate_dob_age()
        day, month, year = map(int, dob.split('/'))
        if month in [4, 6, 9, 11]:
            assert 1 <= day <= 30

def test_generate_dob_age_31_days():
    # Run the test multiple times to ensure 31-day months are handled correctly
    for _ in range(100):
        dob, age = generate_dob_age()
        day, month, year = map(int, dob.split('/'))
        if month in [1, 3, 5, 7, 8, 10, 12]:
            assert 1 <= day <= 31

def test_generate_dob_age_negative_case():
    # Check for any possible invalid date generation
    for _ in range(1000):
        dob, age = generate_dob_age()
        day, month, year = map(int, dob.split('/'))
        try:
            datetime(day=day, month=month, year=year)
        except ValueError:
            pytest.fail(f"Invalid date generated: {dob}")

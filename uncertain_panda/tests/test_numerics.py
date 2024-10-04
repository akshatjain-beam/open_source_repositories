from uncertain_panda import pandas as pd
import pytest
import numpy as np
from tests.fixtures import UncertainPandaTestCase
from uncertain_panda.utils.numerics import value_counts


class TestNumerics(UncertainPandaTestCase):

    def test_coverage_normal(self):
        for sigma in [1, 5, 100]:
            df = pd.Series(np.random.normal(
                np.random.randint(-10, 10), sigma, 2000))
            coverage = df.coverage(0.68)

            # We allow for +- 5% deviation
            self.assertGreater(coverage, 0.95 * sigma)
            self.assertLess(coverage, 1.05 * sigma)

    def test_coverage_uniform(self):
        df = pd.Series(10 * np.random.rand(10000))

        # We also allow for a small deviation here
        self.assertLess(abs(df.coverage(1.0) - 5), 0.1)
        self.assertLess(abs(df.coverage(0.5) - 2.5), 0.1)
        self.assertLess(abs(df.coverage(0.2) - 1.0), 0.1)

    def test_dataframe_coverage(self):
        df = pd.DataFrame({"a": np.random.normal(np.random.randint(-10, 10), 5, 2000),
                           "b": np.random.normal(np.random.randint(-10, 10), 5, 2000)})

        coverage = df.coverage(0.68)
        self.assertLess(abs(coverage["a"] - 5), 0.5)
        self.assertLess(abs(coverage["b"] - 5), 0.5)


class UncertaintyCalculator:
    """Mock class for uncertainty calculations.

    Simulates the behavior of uncertainty calculations by always returning
    a constant value of 0.25 for mean calculations.
    """

    def mean(self, *args, **kwargs):
        """Return a constant mean value for testing purposes.

        Returns:
            float: Constant value of 0.25 for predictable test results.
        """
        return 0.25


class MockSeries:
    """Mock class that simulates a Series with uncertainty calculations.

    Attributes:
        data: The underlying data for the series.
        unc: An UncertaintyCalculator instance for uncertainty computations.
    """

    def __init__(self, data):
        """Initialize the MockSeries with data and uncertainty calculator.

        Args:
            data: Input data for the series.
        """
        self.data = data
        self.unc = UncertaintyCalculator()

    def __eq__(self, other):
        """Compare this series with another value.

        Args:
            other: Value to compare against.

        Returns:
            MockSeries: A new MockSeries containing the comparison results.
        """
        return MockSeries(self.data == other)

    def __iter__(self):
        """Provide iterator over the series data.

        Returns:
            iterator: Iterator over the underlying data.
        """
        return iter(self.data)

    def __len__(self):
        """Get the length of the series.

        Returns:
            int: Number of elements in the series.
        """
        return len(self.data)


@pytest.fixture
def sample_data():
    """Fixture providing sample data for tests.

    Returns:
        MockSeries: A series containing ['A', 'B', 'A', 'C'] with uncertainty calculations.
    """
    return MockSeries(['A', 'B', 'A', 'C'])


def test_basic_value_counts(sample_data):
    """Test basic functionality of value_counts without normalization.

    Verifies that value_counts produces correct counts and index properties
    when called with default parameters.

    Args:
        sample_data: Fixture providing test data.
    """
    result = value_counts(sample_data)

    assert isinstance(result, pd.Series)
    assert set(result.index) == {'A', 'B', 'C'}
    assert isinstance(result.index, pd.CategoricalIndex)
    assert all(result == 1.0)  # 0.25 * 4 = 1.0


def test_normalized_value_counts(sample_data):
    """Test value_counts with normalization enabled.

    Verifies that value_counts produces correct normalized values
    when normalize=True.

    Args:
        sample_data: Fixture providing test data.
    """
    result = value_counts(sample_data, normalize=True)

    assert isinstance(result, pd.Series)
    assert set(result.index) == {'A', 'B', 'C'}
    assert isinstance(result.index, pd.CategoricalIndex)
    assert all(result == 0.25)


def test_empty_data():
    """Test value_counts behavior with empty input data.

    Verifies that value_counts handles empty series correctly.
    """
    empty_data = MockSeries([])
    result = value_counts(empty_data)

    assert isinstance(result, pd.Series)
    assert len(result) == 0


def test_single_value():
    """Test value_counts behavior with a single value.

    Verifies that value_counts correctly handles series containing only one value.
    """
    single_data = MockSeries(['A'])
    result = value_counts(single_data)

    assert isinstance(result, pd.Series)
    assert len(result) == 1
    assert 'A' in result.index
    assert result.iloc[0] == 0.25


def test_args_kwargs_passing(sample_data):
    """Test proper passing of additional arguments to uncertainty calculations.

    Verifies that arbitrary arguments are correctly passed through to the
    underlying uncertainty calculator.

    Args:
        sample_data: Fixture providing test data.
    """
    result = value_counts(sample_data, 'test_arg', key='test_kwarg')
    assert isinstance(result, pd.Series)
    assert len(result) == 3


@pytest.mark.parametrize("input_data,normalize,expected_len", [
    (MockSeries(['A', 'A', 'B']), False, 2),
    (MockSeries(['A', 'B', 'C', 'D']), True, 4),
    (MockSeries(['A']), False, 1),
])
def test_parametrized_value_counts(input_data, normalize, expected_len):
    """Test value_counts with various input combinations.

    Parametrized test that verifies value_counts behavior with different
    input data configurations and normalization settings.

    Args:
        input_data: Test input data.
        normalize: Whether to normalize the counts.
        expected_len: Expected length of the result.
    """
    result = value_counts(input_data, normalize=normalize)
    assert isinstance(result, pd.Series)
    assert len(result) == expected_len


def test_categorical_properties(sample_data):
    """Test categorical properties of the resulting index.

    Verifies that the index of the result has the expected categorical
    properties and contains the correct categories.

    Args:
        sample_data: Fixture providing test data.
    """
    result = value_counts(sample_data)

    assert isinstance(result.index.dtype,
                      pd.CategoricalDtype), "Index is not a categorical dtype"
    assert set(result.index.categories) == {'A', 'B', 'C'}
    assert not result.index.ordered

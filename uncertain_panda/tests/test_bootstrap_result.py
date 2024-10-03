import pytest
import pandas as pd
import numpy as np

from uncertain_panda.uncertainties.bootstrap_result import BootstrapResult

# Sample data for testing
@pytest.fixture
def bootstrap_result():
    """
    Fixture to create a sample BootstrapResult object for testing.
    This creates a bootstrap sample array from a normal distribution with mean 10 and standard deviation 2.
    The nominal value is the mean of the bootstrap samples.
    """
    bootstrap_samples = np.random.normal(loc=10, scale=2, size=1000)  # 1000 samples from a normal distribution
    nominal_value = bootstrap_samples.mean()  # Nominal value as mean of samples
    return BootstrapResult(nominal_value, bootstrap_samples)

def test_ci_symmetric(bootstrap_result):
    """
    Test symmetric confidence interval with default parameter.
    
    This test converts the bootstrap samples to a pandas Series within the test.
    It then tests the symmetric confidence interval with a=0.95.
    It verifies the structure of the returned Series and ensures that the left bound is less than the right bound.
    The nominal value is also checked to be approximately equal to the mean of the bootstrap samples.
    """
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    # Test symmetric confidence interval
    ci_result = bootstrap_result.ci(a=0.95)
    
    # Check the length of the returned Series
    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    # Verify that the left and right bounds make sense
    assert ci_result['left'] < ci_result['right']
    assert ci_result['value'] == pytest.approx(bootstrap_result.nominal_value, rel=1e-2)  # nominal value check

def test_ci_asymmetric(bootstrap_result):
    """
    Test asymmetric confidence interval with specified parameters.
    
    This test converts the bootstrap samples to a pandas Series within the test.
    It then tests the asymmetric confidence interval with a=0.1 and b=0.9.
    It verifies the structure of the returned Series and ensures that the left bound is less than the right bound.
    The nominal value is also checked to be approximately equal to the mean of the bootstrap samples.
    """
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    # Test asymmetric confidence interval
    ci_result = bootstrap_result.ci(a=0.1, b=0.9)  # a=0.1 (10th percentile), b=0.9 (90th percentile)

    # Check the length of the returned Series
    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    # Verify that the left and right bounds make sense
    assert ci_result['left'] < ci_result['right']
    assert ci_result['value'] == pytest.approx(bootstrap_result.nominal_value, rel=1e-2)  # nominal value check

def test_ci_no_parameter(bootstrap_result):
    """
    Test confidence interval with default parameters.
    
    This test converts the bootstrap samples to a pandas Series within the test.
    It then tests the confidence interval with default parameters.
    It verifies the structure of the returned Series and ensures that the left bound is less than the right bound.
    The nominal value is also checked to be approximately equal to the mean of the bootstrap samples.
    """
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    # Test confidence interval with no parameters (defaults)
    ci_result = bootstrap_result.ci()

    # Check the length of the returned Series
    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    # Verify that the left and right bounds make sense
    assert ci_result['left'] < ci_result['right']
    assert ci_result['value'] == pytest.approx(bootstrap_result.nominal_value, rel=1e-2)  # nominal value check

def test_ci_small_sample():
    """
    Test confidence interval with a small sample size.
    
    This test creates a small bootstrap sample array with only 10 samples from a normal distribution.
    It converts the bootstrap samples to a pandas Series within the test.
    It then tests the confidence interval with a=0.95.
    It verifies the structure of the returned Series and ensures that the left bound is less than the right bound.
    """
    bootstrap_samples = np.random.normal(loc=10, scale=2, size=10)  # Only 10 samples
    nominal_value = bootstrap_samples.mean()
    bootstrap_result = BootstrapResult(nominal_value, bootstrap_samples)
    
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    ci_result = bootstrap_result.ci(a=0.95)

    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    assert ci_result['left'] < ci_result['right']

def test_ci_with_outliers():
    """
    Test confidence interval with outliers in the bootstrap samples.
    
    This test creates a bootstrap sample array with significant outliers by combining two normal distributions.
    It converts the bootstrap samples to a pandas Series within the test.
    It then tests the confidence interval with a=0.95.
    It verifies the structure of the returned Series and ensures that the left bound is less than the right bound.
    """
    bootstrap_samples = np.concatenate([np.random.normal(loc=10, scale=2, size=950), np.random.normal(loc=30, scale=5, size=50)])
    nominal_value = bootstrap_samples.mean()
    bootstrap_result = BootstrapResult(nominal_value, bootstrap_samples)
    
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    ci_result = bootstrap_result.ci(a=0.95)

    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    assert ci_result['left'] < ci_result['right']

def test_ci_edge_case_zero_variance():
    """
    Test confidence interval with zero variance in the bootstrap samples.
    
    This test creates a bootstrap sample array with zero variance by having all values the same.
    It converts the bootstrap samples to a pandas Series within the test.
    It then tests the confidence interval with a=0.95.
    It verifies the structure of the returned Series and ensures that the left and right bounds are equal to the common sample value.
    """
    bootstrap_samples = np.full(1000, 10.0)  # 1000 samples with the same value
    nominal_value = bootstrap_samples.mean()
    bootstrap_result = BootstrapResult(nominal_value, bootstrap_samples)
    
    bootstrap_result._bootstrap = pd.Series(bootstrap_result._bootstrap)
    
    ci_result = bootstrap_result.ci(a=0.95)

    assert len(ci_result) == 3
    assert 'value' in ci_result
    assert 'left' in ci_result
    assert 'right' in ci_result

    assert ci_result['left'] == ci_result['right'] == 10.0

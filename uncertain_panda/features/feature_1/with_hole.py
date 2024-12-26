import pandas as pd

from ..utils.numerics import ONE_SIGMA

import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from uncertainties.core import Variable


def _apply_bs(x):
    try:
        return x.bs()
    except AttributeError:
        return x


class BootstrapResult(Variable):
    """
    Result of any calculation performed with the `unc` wrapper.
    It is an instance of :class:`uncertainties.core.Variable`, so
    it behaves like a normal number with uncertainties.
    """
    def __init__(self, nominal_value, bootstrap):
        self._bootstrap = bootstrap

        super().__init__(nominal_value, self.bs().std())

    def bs(self):
        """
        Return the full data sample of bootstrapped results.
        Usually used for visualisations, such as::

            df["var"].unc.mean().bs().plot(kind="hist")
        """
        return self._bootstrap

    def ci(self, a=ONE_SIGMA / 100, b=None):
        """
        Return the confidence interval based on bootstrapped results.

        This method calculates the confidence interval [left, right] such that
        a fraction ``a`` of the bootstrapped results falls below ``left`` and
        a fraction ``b`` of the results falls above ``right``. 

        If `b` is None, the symmetric interval is calculated as follows:
            - left = (1 - a) / 2
            - right = (1 + a) / 2
        Else, provide
            - `a` to left
            - `b` to right

        Parameters:
        a : float, optional
            The fraction of results to be excluded from the lower tail. 
            Default is ONE_SIGMA / 100.
        b : float, optional
            The fraction of results to be excluded from the upper tail. 
            If None, it defaults to the same value as ``a`` for a symmetric interval.

        Returns:
        pd.Series
            A pandas Series containing three elements:
            - 'value': the nominal value of the statistic.
            - 'left': the lower bound of the confidence interval.
            - 'right': the upper bound of the confidence interval.

        Notes:
        - The method utilizes bootstrapping to generate the quantiles.
        - Ensure that the bootstrapped results are available via the `bs` method before calling `ci`.
        """
        $PlaceHolder$


    def strip(self):
        """
        This result still includes the full sample of bootstrapped results.
        So it can be quite heavy (in terms of memory).
        The function returns an uncertainty number without the bootstrapped histogram.
        """
        return Variable(self.nominal_value, self.std_dev)

    def compare_lt(self, rhs):
        """How many of the values are < than ``rhs``?"""
        return (self.bs() < _apply_bs(rhs)).mean()

    def compare_le(self, rhs):
        """How many of the values are <= than ``rhs``?"""
        return (self.bs() <= _apply_bs(rhs)).mean()

    def compare_gt(self, rhs):
        """How many of the values are > than ``rhs``?"""
        return (self.bs() > _apply_bs(rhs)).mean()

    def compare_ge(self, rhs):
        """How many of the values are >= than ``rhs``?"""
        return (self.bs() >= _apply_bs(rhs)).mean()

    def prob(self, value):
        """
        Return the probability to have a resut equal or greater than ``value``.

        If we assume the bootstrapped results are a probability density function,
        this is equivalent to the p-value.
        """
        return self.compare_gt(value)
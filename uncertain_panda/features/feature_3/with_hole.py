from functools import partial

import numpy as np
import pandas as pd

ONE_SIGMA = 68.2689


def pandas_coverage(df, cl=ONE_SIGMA/100):
    if isinstance(df, pd.DataFrame):
        return df.apply(partial(coverage, cl=cl))
    else:
        return coverage(df, cl=cl)


def value_counts(df, *args, normalize=False, **kwargs):
    """
        Returns a Series containing counts of unique rows in the DataFrame.

        Parameters
        df : pandas.DataFrame
            The input DataFrame.

        *args
            Variable number of arguments to pass to the `unc.mean` method.

        normalize : bool, optional
            If True, returns the frequencies of unique rows. Default is False.

        **kwargs
            Additional keyword arguments to pass to the `unc.mean` method.

        Returns
        -------
        pandas.Series
            A Series containing counts of unique rows in the DataFrame, indexed by a CategoricalIndex of unique values.

        Notes
        -----
        - This function uses the `unc.mean` method to calculate the mean of the uncertainty values for each unique row.
        - If `normalize` is True, the function returns the  frequencies of unique rows, which can be useful for comparing the distribution of values across different DataFrames.
        - The function assumes that the input DataFrame contains uncertainty values that can be used to calculate the mean.
    """
    $PlaceHolder$



def coverage(series, cl=0.68):
    series = series[~np.isnan(series)]

    if len(series) == 0:
        return np.NAN  # pragma: no cover

    centered_dist = np.abs(series - np.median(series))
    b = np.percentile(centered_dist, 100 * cl)
    return b

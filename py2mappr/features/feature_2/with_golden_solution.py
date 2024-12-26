```
def find_node_color_attr(df: pd.DataFrame) -> str:
    """
    Finds the most likely column to be used as the color attribute for nodes.
    The column is determined by the following criteria:

    1. The column must be numeric.

    2. The column must have the least distinct values.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    Returns
    -------
    `str`: The name of the column that is most likely to be used as the color
    attribute for nodes.
    """
    unique_counts = df.nunique()
    lowest_distinct = unique_counts.min()
    lowest_distinct_columns = unique_counts[
        unique_counts == lowest_distinct
    ].index.tolist()

    return _find_most_filled_column(df, lowest_distinct_columns)
```
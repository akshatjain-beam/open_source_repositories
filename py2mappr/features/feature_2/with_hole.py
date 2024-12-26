from typing import List, Tuple, Union
import pandas as pd
import numpy as np
import warnings

images = ["image", "picture", "photo", "img", "img_url", "imgurl"]
labels = ["originallabel", "name", "title", "label"]


def _find_most_filled_column(df: pd.DataFrame, column_names: List[str]) -> str:
    non_empty = df[column_names]
    non_empty = non_empty.isnull().sum()

    return non_empty.sort_values(ascending=True).index[0]


def find_node_image_attr(df: pd.DataFrame) -> str:
    """
    Finds the most likely column to be used as the image attribute for nodes.
    The column is determined by the following criteria:

    1. The column name must contain one of the following words: image, picture,
    photo, img, img_url, imgurl.

    2. The column must have the most non-empty values.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    Returns
    -------
    `str`: The name of the column that is most likely to be used as the image
    attribute for nodes.

    """
    columns: List[str] = df.columns.values.tolist()

    match_columns = [col for col in columns if col.lower() in images]

    if len(match_columns) == 0:
        return None

    return _find_most_filled_column(df, match_columns)


def find_node_label_attr(df: pd.DataFrame) -> str:
    """
    Finds the most likely column to be used as the label attribute for nodes.
    The column is determined by the following criteria:

    1. The column name must contain one of the following words: originallabel,
    name, title, label.

    2. The column must have the most non-empty values.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    Returns
    -------
    `str`: The name of the column that is most likely to be used as the label
    attribute for nodes.
    """
    columns: List[str] = df.columns.values.tolist()

    match_columns = [col for col in columns if col.lower() in labels]

    if len(match_columns) == 0:
        return None

    return _find_most_filled_column(df, match_columns)


def find_node_size_attr(df: pd.DataFrame, exclude: List[str] = []) -> str:
    """
    Finds the most likely column to be used as the size attribute for nodes.
    The column is determined by the following criteria:

    1. The column must be numeric.

    2. The column must have the most non-empty values.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    exclude: List[str]. A list of column names to exclude from the search.

    Returns
    -------
    `str`: The name of the column that is most likely to be used as the size
    attribute for nodes.
    """
    columns = [
        col
        for col in df.select_dtypes(include=np.number).columns.tolist()
        if col.lower() not in exclude
    ]

    if len(columns) == 0:
        return None

    return _find_most_filled_column(df, columns)



"""
Create a function `find_node_color_attr` that identifies the most suitable column to be used as the color attribute for nodes in a graph.

The selection criteria for the column are as follows:

1. Among the columns, the one with the least number of distinct values is preferred.
2. Among all the preferred columns, the columns with least Null values are selected using function `_find_most_filled_column`.

Parameters
df : pd.DataFrame
    The DataFrame to be analyzed for potential color attributes.

Returns
str
    The name of the column that is most likely to be used as the color attribute for nodes.
    If no suitable column is found, an empty string is returned.
"""
$PlaceHolder$


def find_node_xy_attr(
    df: pd.DataFrame, pattern_x="x", pattern_y="y"
) -> Union[Tuple[str, str], Tuple[None, None]]:
    """
    Finds the most likely columns to be used as the x and y coordinates for
    nodes. It first checks for columns with the names x and y. If none are
    found, it case-insensitive checks for columns with the names *x* and *y*
    where * is any character. If none are found, it returns None for both x and
    y. The columns are determined by the following criteria:

    1. The column name must contain one of the following words: x, y.

    2. The column must have the most non-empty values.

    Parameters
    ----------
    df: DataFrame. The data frame to be analyzed.

    pattern_x: str. The pattern to search for in the column names to identify
    the x coordinate.

    pattern_y: str. The pattern to search for in the column names to identify
    the y coordinate.

    Returns
    -------
    `Tuple[str, str]`: The name of the columns that are most likely to be used
    as the x and y coordinates for nodes.
    """
    columns = df.columns.tolist()
    basic_x = [col for col in columns if col.lower() in pattern_x]
    basic_y = [col for col in columns if col.lower() in pattern_y]
    if len(basic_x) == 1 and len(basic_y) == 1:
        return basic_x[0], basic_y[0]

    xcolumns = [col for col in columns if pattern_x in col.lower()]

    if len(xcolumns) == 0:
        warnings.warn(
            f"No columns found with {pattern_x} in the name. X,Y coordinates must be specified explicitly"
        )
        return None, None

    for col in xcolumns:
        ycol_name = col.lower().replace(pattern_x, pattern_y)
        for ycol in columns:
            if ycol.lower() == ycol_name:
                return col, ycol

    return None, None

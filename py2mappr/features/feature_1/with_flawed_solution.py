```
def calculate_attr_types(df: pd.DataFrame) -> Dict[str, ATTR_TYPE]:
    """
    Create a function `calculate_attr_types` that's Calculates the attribute types of the columns of the given data frame.
    Based on the data type of the column, the attribute type is determined. If
    the column is a number, it is further analyzed to determine if it is a
    year, timestamp, integer or float. If the column is a string, it is further
    analyzed to determine if it is a list of strings or a single string.

    If column is of a number type, it  it uses `_detect_number_column`. to checks the values of the column in the
    data frame. If the values are all integers, it is an `integer`. If the
    values are all floats, it is a `float`. If the values are all years, i.e.
    all values fall in range between 1800 and 2100, it is a `year`. If the
    values are all timestamps, i.e. all values fall in range between 1000000000
    and 9999999999, it is a `timestamp`. 
    If the column is a string, it checks the values of the column in the data
    frame. If the values are all strings, it is a `string`. If the values are
    all lists of strings, i.e. any value contains a character '|', it is a
    `liststring`.

    Parameters
    df: DataFrame. The data frame to be analyzed.

    Returns
    `Dict[str, ATTR_TYPE]`: A dictionary with the column names as keys and the
    attribute types as values.
    """
    attr_types = dict()
    # for each column, determine the type of attribute it is
    for column in df.columns.values:
        if df[column].dtype in [np.float64, np.int64, np.float32, np.int32]:
            attr_types[column] = _detect_number_column(df, column)
        elif df[column].dtype == object and any(
            "|" in str(x) for x in df[column]
        ):
            attr_types[column] = "liststring"
        elif df[column].dtype == object:
            attr_types[column] = "string"
        else:
            attr_types[column] = "unknown"
    return attr_types
```
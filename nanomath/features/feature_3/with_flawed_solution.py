```
from collections import namedtuple

def get_top_5(df, col, values, fill='quals'):
    """Retrieve the top 5 rows from a DataFrame based on a specified column.

    Parameters:
    - df (pandas.DataFrame): The DataFrame from which to extract data.
    - col (str): The name of the column used for sorting the DataFrame.
    - values (list of str): A list of column names to include in the output.
    - fill (bool): If True, adds a 'fill' column initialized to zero. Default is False.

    Returns:
    - tuple: An iterator of named tuples representing the top 5 rows, 
              including specified columns and an optional 'fill' column.

    Notes:
    - If the DataFrame contains a column named 'readIDs', it will be appended 
     to the 'values' parameter.
    - The DataFrame is reset to a zero-based index after sorting and selecting the top 5 rows.
    
    """
    if "readIDs" in df:
        values.append("readIDs")
    tmp = df.sort_values(by=col, ascending=False).reset_index(drop=True)
    top5 = tmp.loc[:4, values]
    nt = namedtuple('top5', values + ([fill] if fill else []))
    return (nt(*r) if len(r) == len(values)
            else nt(*r, fill=0) for r in top5.values.tolist())
```
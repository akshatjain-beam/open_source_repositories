```
    # Calculate the mean of the uncertainty values for each unique row
    df['mean'] = df.apply(lambda row: row.unc.mean(*args, **kwargs), axis=1)
    
    # Count the occurrences of each unique row
    unique_rows = df.apply(tuple, axis=1).unique()
    counts = pd.Series(
        [len(df[df.apply(tuple, axis=1) == row]) for row in unique_rows],
        index=pd.CategoricalIndex(unique_rows),
    )
    if normalize:
        counts = counts / counts.sum()
    return counts
```
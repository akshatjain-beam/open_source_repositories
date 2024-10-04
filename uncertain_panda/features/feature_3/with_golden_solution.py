```
    possible_values = set(df)
    normalization = len(df)

    if normalize:
        normalization = 1

    count = {
        val: (df == val).unc.mean(*args, **kwargs) * normalization
        for val in possible_values
    }
    return pd.Series(count, index=pd.CategoricalIndex(possible_values))
```
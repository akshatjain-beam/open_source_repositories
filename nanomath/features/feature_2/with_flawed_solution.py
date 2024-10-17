```
    return df[np.abs(df[columnname] - df[columnname].median()) <= 3 * df[columnname].std()]
```
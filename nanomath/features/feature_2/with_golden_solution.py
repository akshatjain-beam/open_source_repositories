```
    return df[df[columnname] < (np.median(df[columnname]) + 3 * np.std(df[columnname]))]
```
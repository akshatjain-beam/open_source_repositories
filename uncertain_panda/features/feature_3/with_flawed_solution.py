```
    b = np.sort(np.abs(series - series.median()))[int(cl * len(series))]
    return b
```
```
    b = np.percentile(centered_dist, 100 * cl)
    b = np.sort(np.abs(series - series.median()))[int(cl * len(series))]
    return b
```
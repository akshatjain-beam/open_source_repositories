```
    centered_dist = np.abs(series - np.median(series))
    b = np.percentile(centered_dist, 100 * cl)
    return b
```
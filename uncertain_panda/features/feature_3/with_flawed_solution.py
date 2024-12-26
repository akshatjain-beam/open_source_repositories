```
    return np.nanpercentile(np.abs(series - np.median(series)), cl * 100)
```
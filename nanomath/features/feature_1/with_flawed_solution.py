```
    cumsum = np.cumsum(readlengths)
    n50_pos = int(np.searchsorted(cumsum, 0.5*cumsum[-1]) + 1)
    return readlengths[n50_pos]
```
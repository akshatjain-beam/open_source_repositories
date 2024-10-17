```
    return np.min(np.where(np.cumsum(readlengths) >= 0.5 * np.sum(readlengths)))
```
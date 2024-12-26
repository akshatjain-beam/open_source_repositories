```
    return readlengths[np.where(np.cumsum(readlengths) >= 0.5 * np.sum(readlengths))[0][0]]
```
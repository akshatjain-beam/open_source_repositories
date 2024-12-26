```
    years = list(years)
    return (
        dataset[..., years.index(end)] - dataset[..., years.index(start)]
    ) / dataset[..., years.index(start)]
```
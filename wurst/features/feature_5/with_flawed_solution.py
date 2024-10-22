```
    start_index = years.index(start)
    end_index = years.index(end)
    return (dataset[..., end_index] - dataset[..., start_index]) / dataset[..., start_index]
```
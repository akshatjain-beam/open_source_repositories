```
    for i in range(0, len(string), chunk_size):
        if drop_remaining and i + chunk_size > len(string):
            break
        yield string[i:i + chunk_size]
```
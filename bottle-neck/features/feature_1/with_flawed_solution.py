```
@functools.lru_cache(maxsize=None)
def cached_classproperty(fun):
    return classproperty(property(fun))
```
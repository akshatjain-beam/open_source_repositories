```
def cached_classproperty(fun):
    """Create a cached class property.

    It implements the above `classproperty` decorator, with
    the difference that the function result is computed and attached
    to class as direct attribute. (Lazy loading and caching.)

    Args:
        fun: The method to be cached as a class property.

    Returns:
        A class property that returns the cached value.

    Raises:
        AttributeError: If the cache cannot be initialized.
        KeyError: If the cache does not contain the value.
    """

    @classproperty
    @functools.wraps(fun)
    def cached_property(cls):
        cached_name = "_{}".format(fun.__name__)
        if not hasattr(cls, cached_name):
            setattr(cls, cached_name, fun(cls))
        return getattr(cls, cached_name)
    return cached_property
```
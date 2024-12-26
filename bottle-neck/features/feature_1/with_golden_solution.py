```
def cached_classproperty(fun):
    """A memorization decorator for class  properties.

    It implements the above `classproperty` decorator, with
    the difference that the function result is computed and attached
    to class as direct attribute. (Lazy loading and caching.)
    """
    @functools.wraps(fun)
    def get(cls):
        try:
            return cls.__cache[fun]
        except AttributeError:
            cls.__cache = {}
        except KeyError:  # pragma: no cover
            pass
        ret = cls.__cache[fun] = fun(cls)
        return ret
    return classproperty(get)
```
def singleton(cls):
    """Create a decorator called `singleton` that ensures a class has only one instance.
    Ensure thread safety in the implementation.
    """

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            with threading.Lock():
                if not wrapper_singleton.instance:
                    wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton
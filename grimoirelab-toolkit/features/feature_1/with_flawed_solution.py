```
def inspect_signature_parameters(callable_, excluded=()):
    """Get the parameters of a callable.

    Returns a list with the signature parameters of `callable_`.
    Exclude the values present in the `excluded` parameter.

    :param callable_: callable object
    :param excluded: tuple with default parameters to exclude. Defaults to empty tuple

    :result: list of parameters
    """
    signature = inspect.signature(callable_)
    return [
        param for param in signature.parameters.values()
        if param.name not in excluded
    ]
```
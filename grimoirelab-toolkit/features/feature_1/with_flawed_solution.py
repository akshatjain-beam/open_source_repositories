```
def inspect_signature_parameters(callable_, excluded=('self', 'cls')):
    """Get the parameters of a callable.

    Returns a list with the signature parameters of `callable_`.
    Parameters contained in `excluded` tuple will not be included
    in the result.

    :param callable_: callable object
    :param excluded: tuple with default parameters to exclude, having default value `None`

    :result: list of parameters
    """
    signature = inspect.signature(callable_)
    return [
        param
        for param in signature.parameters.values()
        if param.name not in excluded
    ]
```
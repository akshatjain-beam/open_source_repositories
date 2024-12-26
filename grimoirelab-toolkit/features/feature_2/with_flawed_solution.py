```
    params = inspect_signature_parameters(callable_, excluded=excluded)
    is_varargs = any(p.kind is inspect.Parameter.VAR_POSITIONAL
                   for p in params)
    is_varkwargs = any(p.kind is inspect.Parameter.VAR_KEYWORD
                    for p in params)

    result = {}
    for param in params:
        name = param.name
        if name in candidates:
            result[name] = candidates[name]
        elif param.default is not inspect.Parameter.empty:
            result[name] = param.default
        elif is_varargs:
            result = candidates
        elif is_varkwargs:
            result.update(candidates)
        else:
            raise AttributeError(
                "Parameter '{}' not found for '{}'".format(name,
                                                         callable_.__name__)
            )

    return result
```
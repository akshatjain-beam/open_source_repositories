```
    signature_params = inspect_signature_parameters(callable_,
                                                    excluded=excluded)
    exec_params = {}

    add_all = False
    for param in signature_params:
        name = param.name

        if str(param).startswith('*'):
            add_all = True
        elif name in candidates:
            exec_params[name] = candidates[name]
        elif param.default == inspect.Parameter.empty:
            msg = "required argument %s not found" % name
            raise AttributeError(msg, name)
        else:
            continue

    if add_all:
        exec_params = candidates

    return exec_params
```
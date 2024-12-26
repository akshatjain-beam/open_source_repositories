```
    """Link internal exchanges by ``fields``. Creates ``input`` field in newly-linked exchanges."""
    input_databases = get_input_databases(data)
    get_tuple = lambda exc: tuple([exc[f] for f in fields])
    products = {
        get_tuple(reference_product(ds)): (ds["database"], ds["code"]) for ds in data
    }

    for ds in data:
        for exc in ds["exchanges"]:
            if exc.get("input"):
                continue

            if exc["type"] == "biosphere":
                raise ValueError(
                    "Unlinked biosphere exchange:\n{}".format(pformat(exc))
                )

            try:
                exc["input"] = products[get_tuple(exc)]
            except KeyError:
                raise KeyError(
                    "Can't find linking activity for exchange:\n{}".format(pformat(exc))
                )
    return data
```
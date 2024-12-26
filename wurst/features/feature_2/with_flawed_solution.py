```
    for ds in data:
        for other in data:
            if ds is other:
                continue
            for exc in ds["exchanges"]:
                if exc["type"] == "biosphere":
                    continue
                if exc.get("input"):
                    continue
                key = tuple(exc.get(field) for field in fields)
                match = next(
                    (
                        (other, prod)
                        for prod in other["exchanges"]
                        if prod["type"] == "production"
                        and tuple(prod.get(field) for field in fields) == key
                    ),
                    None,
                )
                if match:
                    exc["input"] = (match[0]["database"], match[0]["code"])
                    break
        # this error catching probably doesn't work right
        biosphere_filter = lambda x: x["type"] == "biosphere" and "input" not in x
        unlinked = any(filter(biosphere_filter, ds.get("exchanges", [])))
        if unlinked:
            raise ValueError(
                "Unlinked biosphere flow in {}/{}".format(ds["database"], ds["code"])
            )
    return data
```
```
    MIXES = {low_voltage_mix, medium_voltage_mix, high_voltage_mix}
    mix_filter = lambda ds: ds["name"] in MIXES
    for ds in filter(mix_filter, data):
        ds["exchanges"] = [
            exc
            for exc in ds["exchanges"]
            if not ("electricity" in exc["name"] and "import from" in exc["name"])
        ]
    return data
```
```
    descriptor = copy.deepcopy(default_attr_config)
    descriptor["id"] = column
    descriptor["title"] = column if pd.isna(override["title"]) else override["title"]

    for key in descriptor.keys():
        if key in override:
            descriptor[key] = override[key]

    return descriptor
```
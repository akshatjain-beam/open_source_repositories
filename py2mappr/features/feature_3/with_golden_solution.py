```
    attrs: AttributeConfig = dict(copy.deepcopy(default_attr_config))

    # if title doesnt exist. copy from id.
    attrs["id"] = column
    attrs["title"] = attrs["id"] if attrs["title"] == "" else attrs["title"]

    # use if override exists
    if override is not None:
        for key, val in override.items():
            if key in attrs:
                attrs[key] = val

    return attrs
```
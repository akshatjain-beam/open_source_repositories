```
    if items is not None:
      source = {k[len(prefix):]: v
                for k, v in items
                if isinstance(k, str) and k.startswith(prefix)}
    else:
      source = {attr[len(prefix):]: getattr(source, attr)
                for attr in properties(source)
                if isinstance(attr, str) and attr.startswith(prefix)}
```
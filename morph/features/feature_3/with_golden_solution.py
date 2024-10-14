```
    if items is not None:
      source = {k[len(prefix):]: v
                for k, v in items
                if getattr(k, 'startswith', lambda x: False)(prefix)}
    else:
      source = {attr[len(prefix):]: getattr(source, attr)
                for attr in properties(source)
                if attr.startswith(prefix)}
```
```
return \
    not isstr(obj) \
    and not isdict(obj) \
    and ( isinstance(obj, (list, tuple)) \
          or callable(getattr(obj, '__iter__', None)))
```
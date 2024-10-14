```
  return \
    not isstr(obj) \
    and ( isinstance(obj, (list, tuple)) \
          or ( hasattr(obj, '__getitem__') \
               and hasattr(obj, '__iter__') ))
```
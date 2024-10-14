```
isdict(obj):
  '''
  Returns True if `obj` is a dict-like object (but not a string or
  list); i.e. a dict, subclass thereof, or having an interface that
  supports key, value, and item iteration.
  '''
  return \
    not isstr(obj) \
    and ( isinstance(obj, dict) \
          or ( callable(getattr(obj, 'keys', None)) \
               and callable(getattr(obj, 'values', None)) \
               and callable
```
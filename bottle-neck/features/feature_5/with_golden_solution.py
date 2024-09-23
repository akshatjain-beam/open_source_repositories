```
        method = getattr(cls, status_line.lower()[4:].replace(' ', '_'))
        return method(msg)
```
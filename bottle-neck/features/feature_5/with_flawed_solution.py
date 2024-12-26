```
        return getattr(cls, status_line.lower().replace(' ', '_').replace(status_line.split(' ')[0], ''), cls.bad_request)(msg)
```
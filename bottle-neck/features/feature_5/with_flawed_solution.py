```
        return cls(
            status_code=int(status_line.split(' ', 1)[0]),
            errors=[msg] if msg else [status_line]
        )
```
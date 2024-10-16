```
		status_line = status_line.lower().replace(' ', '_')
		status_line = ''.join(
		    ch for ch in status_line if ch.isalnum() or ch == '_'
		)
		method = getattr(cls, status_line, cls.not_implemented)
		return method(errors=msg)
```
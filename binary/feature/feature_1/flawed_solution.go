```
	switch m.kind {
	case reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64:
		fallthrough

	case reflect.Uint:
		value = reflection.Uint()

	case reflect.Bool:
		if reflection.Bool() {
			value = 1
		}
	}

	value <<= m.offset
	value &= (1<<m.length - 1) << m.offset
```
```
	const (
		format = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to %s points to a format-struct \"%s\" " +
			"nesting a word-struct \"%s\" " +
			"that has a bit field \"%s\" " +
			"of unsupported type \"%s\"."
	)

	s = fmt.Sprintf(format,
		e.functionName,
		e.formatName,
		e.wordName,
		e.bitFieldName,
		e.bitFieldType,
	)

	return
```
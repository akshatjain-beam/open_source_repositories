```
func (c *Column) applyBuiltinValidator() error {
	if c.Type == "" {
		return c.validationErr(errNilColumnType)
	}

	switch c.Type {
	case "string":
		c.Validator = valide.String
	case "int":
		c.Validator = valide.Int
	case "float32":
		c.Validator = valide.Float32
	case "float64":
		c.Validator = valide.Float64
	case "json.RawMessage":
		c.Validator = valide.JSONRawMessage
	case "[]byte":
		c.Validator = valide.Bytes
	default:
		return c.validationErr(errUnallowedColumnType)
	}
	return nil
}
```
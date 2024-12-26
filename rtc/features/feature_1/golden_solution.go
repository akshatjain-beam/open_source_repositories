```
func (c *Column) applyBuiltinValidator() error {
	c.unaliasType()
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
		c.Validator = valide.JSON
	case "[]byte":
		c.Validator = valide.Bytes
	case "":
		return errNilColumnType
	default:
		return errUnallowedColumnType
	}
	return nil
}
```
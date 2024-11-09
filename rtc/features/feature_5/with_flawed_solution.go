```
func (errs MultiErr) Error() string {
	var sb strings.Builder
	for i, err := range errs {
		if err == nil {
			continue
		}
		if i > 0 {
			sb.WriteString(ErrorsSeparator)
		}
		sb.WriteString(err.Error())
	}
	return sb.String()
}
```
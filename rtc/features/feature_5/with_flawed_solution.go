```
func (errs MultiErr) Error() string {
	var str string
	for _, err := range errs {
		if err == nil {
			continue
		}
		if str != "" {
			str += ErrorsSeparator
		}
		str += err.Error()
	}
	return str
}
```
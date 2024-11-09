```
func (errs MultiErr) Error() string {
	var strBaseErr string
	for _, err := range errs {
		if err == nil {
			continue
		}
		strBaseErr += err.Error()
		strBaseErr += ErrorsSeparator
	}
	return strBaseErr
}
```
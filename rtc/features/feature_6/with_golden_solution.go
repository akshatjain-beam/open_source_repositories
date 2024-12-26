```
var fullVErrRegex = regexp.MustCompile(`validation error: (.*). At`)
var tinyVErrRegex = regexp.MustCompile(`validation error: (.*)`)

func UnwrapValidationError(vErr error) error {
	if vErr == nil || vErr.Error() == "" {
		return nil
	}
	strErr := vErr.Error()
	var vErrRegex *regexp.Regexp
	if strings.Contains(strErr, ". At") {
		vErrRegex = fullVErrRegex
	} else {
		vErrRegex = tinyVErrRegex
	}
	strErr = vErrRegex.FindAllString(strErr, 1)[0]
	strErr = strings.TrimSuffix(strings.TrimPrefix(strErr, "validation error: "), ". At")
	return errors.New(strErr)
}
```
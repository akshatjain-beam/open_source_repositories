```
var (
	fullVErrRegex = regexp.MustCompile(`validation error:\s(.*?)\s\. At`) // Matches "validation error: ... . At"
	tinyVErrRegex = regexp.MustCompile(`validation error:\s(.*)`)       // Matches "validation error: ..."
)

func UnwrapValidationError(vErr error) error {
	if vErr == nil {
		return nil
	}

	errStr := vErr.Error()
	if errStr == "" {
		return nil
	}

	var match []string
	if strings.Contains(errStr, ". At") {
		match = fullVErrRegex.FindStringSubmatch(errStr)
	} else {
		match = tinyVErrRegex.FindStringSubmatch(errStr)
	}

	if len(match) > 1 {
		msg := strings.TrimSpace(match[1])
		return errors.New(msg)
	}

	return nil
}
```
```
func ToCamelCase(s string) string {
	s = addWordBoundariesToNumbers(s)
	letters := []rune(strings.Trim(s, " "))
	var n []rune
	shouldCapitalize := false
	for _, letter := range letters {
		if isDelimiter(letter) {
			shouldCapitalize = true
		} else {
			if shouldCapitalize && isLower(letter) {
				letter = letter - 32
				shouldCapitalize = false
			} else if !shouldCapitalize && isUpper(letter) {
				letter = letter + 32
			}
			n = append(n, letter)
		}
	}

	return string(n)
}
```
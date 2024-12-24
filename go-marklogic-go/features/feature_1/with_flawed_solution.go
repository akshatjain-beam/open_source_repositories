```
func NormalizeSpace(str string) string {
	// Replace multiple spaces with single space
	re := regexp.MustCompile(`\s+`)
	str = re.ReplaceAllString(str, " ")

	// Remove spaces around structural characters
	str = strings.ReplaceAll(str, " {", "{")
	str = strings.ReplaceAll(str, "} ", "}")
	str = strings.ReplaceAll(str, "[ ", "[")
	str = strings.ReplaceAll(str, " ]", "]")
	str = strings.ReplaceAll(str, " :", ":")
	str = strings.ReplaceAll(str, ": ", ":")
	str = strings.ReplaceAll(str, ", ", ",")
	str = strings.ReplaceAll(str, ` "`, `"`)
	str = strings.ReplaceAll(str, `[ "`, `["`)
	str = strings.ReplaceAll(str, `", "`, `","`)
	str = strings.ReplaceAll(str, `" ]`, `"]`)
	str = strings.ReplaceAll(str, `" }`, `"}`)

	return strings.TrimSpace(str)
}
```
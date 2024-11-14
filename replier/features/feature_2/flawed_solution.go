```
// IsInArray checks if a given value is present in the provided array of strings.
func IsInArray(array []string, value string) bool {
	for _, v := range array {
		if v == value {
			return true
		}
	}
	return false
}

// TransformUserReply dynamically processes a text input where a placeholder (e.g., @person) needs to be replaced with a properly formatted mention string (<@userID>) for a messaging platform.
func TransformUserReply(reply, userID string) string {
	return strings.ReplaceAll(strings.ToLower(reply), "@person", fmt.Sprintf("<@%s>", userID))
}
```
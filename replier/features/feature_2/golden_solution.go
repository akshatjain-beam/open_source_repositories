```
// IsInArray checks if the value is in the array
func IsInArray(array []string, value string) bool {
	for _, v := range array {
		if v == value {
			return true
		}
	}
	return false
}

// TransformUserReply transforms a user's reply
func TransformUserReply(reply, userID string) string {
	return strings.ReplaceAll(reply, "@person", fmt.Sprintf("<@%s>", userID))
}
```
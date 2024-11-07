```
	return strings.ReplaceAll(strings.ToLower(reply), "@person", fmt.Sprintf("<@%s>", userID))
```
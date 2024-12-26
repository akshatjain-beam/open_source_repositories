```
func VerifySlackRequest(r *http.Request, body []byte) bool {
	signingSecret := os.Getenv("SLACK_SIGNING_SECRET")
	timestamp := r.Header.Get("X-Slack-Request-Timestamp")
	slackSignature := r.Header.Get("X-Slack-Signature")

	signingString := fmt.Sprintf("v0:%s:%s", timestamp, string(body))

	mac := hmac.New(sha256.New, []byte(signingSecret))
	if _, err := mac.Write([]byte(signingString)); err != nil {
		return false 
	}
	calculatedSignature := "v0=" + hex.EncodeToString(mac.Sum(nil))

	return hmac.Equal([]byte(calculatedSignature), []byte(slackSignature))
}
```
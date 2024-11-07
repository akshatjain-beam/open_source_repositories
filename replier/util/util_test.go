package util

import (
	"net/http"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestVerifySlackRequest(t *testing.T) {
	// Random 32-character string
	secret := "2039f48n09c00249u0riunotiu034he9"
	os.Setenv("SLACK_SIGNING_SECRET", secret)

	r := &http.Request{
		Header: http.Header{
			"X-Slack-Request-Timestamp": {"1596411843"},
			"X-Slack-Signature":         {"v0=bf6cccaf6d49158d589bb82e5ef94778d4c6c39bb4ef3a6cc56fe25426c24eb4"},
		},
	}

	// Example slash command request
	b := []byte("text=hello&user_id=U12345678&team_id=T12345678&command=/test")

	assert.True(t, VerifySlackRequest(r, b))

	// Should fail:
	os.Setenv("SLACK_SIGNING_SECRET", "blahblah")
	assert.False(t, VerifySlackRequest(r, b))
}

func TestIsInArray(t *testing.T) {
	assert.True(t, IsInArray([]string{"i", "like", "go", "!"}, "go"))
	assert.False(t, IsInArray([]string{"i", "like", "go", "!"}, "rust"))
}

func TestTransformUserReply(t *testing.T) {
	assert.Equal(t, "Howdy, <@U12345678>! :wave:", TransformUserReply("Howdy, @person! :wave:", "U12345678"))
}
func TestTransformUserReply_BasicReplacement(t *testing.T) {
    // Test Case 1: Basic replacement of "@person" with a formatted user mention.
    // Input: "Howdy, @person! :wave:"
    // Expected Output: "Howdy, <@U12345678>! :wave:"
    assert.Equal(t, "Howdy, <@U12345678>! :wave:", TransformUserReply("Howdy, @person! :wave:", "U12345678"))
}

func TestTransformUserReply_MixedCasePlaceholder(t *testing.T) {
    // Test Case 2: Placeholder with mixed case ("@Person") should not be replaced.
    // Input: "Hello, @person! How are you?"
    // Expected Output: "Hello, <@U12345678>! How are you?"
    assert.Equal(t, "Hello, <@U12345678>! How are you?", TransformUserReply("Hello, @person! How are you?", "U12345678"))
}

func TestTransformUserReply_MultiplePlaceholders(t *testing.T) {
    // Test Case 3: Multiple occurrences of "@person" in the string should all be replaced with "<@U12345678>".
    // Input: "hi, @person! How is @person123?"
    // Expected Output: "hi, <@U12345678>! How is <@U12345678>123?"
    assert.Equal(t, "hi, <@U12345678>! How is <@U12345678>123?", TransformUserReply("hi, @person! How is @person123?", "U12345678"))
}

func TestTransformUserReply_PlaceholderWithNumbers(t *testing.T) {
    // Test Case 4: Placeholder with numbers (e.g., "@person123") should be replaced leaving 123.
    // Input: "Good morning, @person! Have a nice day @person123."
    // Expected Output: "Good morning, <@U12345678>! Have a nice day <@U12345678>123."
    assert.Equal(t, "Good morning, <@U12345678>! Have a nice day <@U12345678>123.", TransformUserReply("Good morning, @person! Have a nice day @person123.", "U12345678"))
}

func TestTransformUserReply_PunctuationAroundPlaceholder(t *testing.T) {
    // Test Case 5: Placeholder with punctuation (e.g., "@person!") should be replaced, leaving punctuation unchanged.
    // Input: "Welcome! @person! is here!"
    // Expected Output: "Welcome! <@U12345678>! is here!"
    assert.Equal(t, "Welcome! <@U12345678>! is here!", TransformUserReply("Welcome! @person! is here!", "U12345678"))
}

func TestTransformUserReply_EmptyInput(t *testing.T) {
    // Test Case 6: Empty input string should return an empty string, as no transformation is needed.
    // Input: ""
    // Expected Output: ""
    assert.Equal(t, "", TransformUserReply("", "U12345678"))
}

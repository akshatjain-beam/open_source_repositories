package util

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsInArray(t *testing.T) {
    // Test 1: Existing element in the array
    assert.True(t, IsInArray([]string{"i", "like", "go", "!"}, "go"))

    // Test 2: Non-existing element in the array
    assert.False(t, IsInArray([]string{"i", "like", "go", "!"}, "rust"))

    // Test 3: Empty array, should return false for any search
    assert.False(t, IsInArray([]string{}, "any"))

    // Test 4: Element is at the beginning of the array
    assert.True(t, IsInArray([]string{"first", "second", "third"}, "first"))

    // Test 5: Element is at the end of the array
    assert.True(t, IsInArray([]string{"first", "second", "third"}, "third"))

    // Test 6: Array with duplicate values, should return true if value is present
    assert.True(t, IsInArray([]string{"apple", "banana", "apple", "cherry"}, "apple"))

    // Test 7: Case sensitivity check, should return false if the case doesn't match
    assert.False(t, IsInArray([]string{"Hello", "world"}, "hello"))

    // Test 8: Single element array, should return true if the element matches
    assert.True(t, IsInArray([]string{"single"}, "single"))

    // Test 9: Single element array, should return false if the element doesn't match
    assert.False(t, IsInArray([]string{"single"}, "notfound"))

    // Test 10: Special characters in the array, should return true if the value is found
    assert.True(t, IsInArray([]string{"$apple", "@banana", "#cherry"}, "@banana"))
}
func TestVerifySlackRequestWithEmptySecret(t *testing.T) {
	// Set an empty SLACK_SIGNING_SECRET
	os.Setenv("SLACK_SIGNING_SECRET", "")

	r := &http.Request{
		Header: http.Header{
			"X-Slack-Request-Timestamp": {"1596411843"},
			"X-Slack-Signature":         {"v0=bf6cccaf6d49158d589bb82e5ef94778d4c6c39bb4ef3a6cc56fe25426c24eb4"},
		},
	}

	// Example slash command request
	b := []byte("text=hello&user_id=U12345678&team_id=T12345678&command=/test")

	// This should fail because SLACK_SIGNING_SECRET is empty
	assert.False(t, VerifySlackRequest(r, b))
}

func TestVerifySlackRequestWithFutureTimestamp(t *testing.T) {
	// Random 32-character string
	secret := "2039f48n09c00249u0riunotiu034he9"
	os.Setenv("SLACK_SIGNING_SECRET", secret)

	// Future timestamp (e.g., a timestamp from a future date)
	r := &http.Request{
		Header: http.Header{
			"X-Slack-Request-Timestamp": {"9999999999"}, // Future timestamp
			"X-Slack-Signature":         {"v0=bf6cccaf6d49158d589bb82e5ef94778d4c6c39bb4ef3a6cc56fe25426c24eb4"},
		},
	}

	// Example slash command request
	b := []byte("text=hello&user_id=U12345678&team_id=T12345678&command=/test")

	// This should fail because the timestamp is in the future
	assert.False(t, VerifySlackRequest(r, b))
}

func TestVerifySlackRequestWithMissingSignatureHeader(t *testing.T) {
	// Random 32-character string
	secret := "2039f48n09c00249u0riunotiu034he9"
	os.Setenv("SLACK_SIGNING_SECRET", secret)

	r := &http.Request{
		Header: http.Header{
			"X-Slack-Request-Timestamp": {"1596411843"},
			// Missing X-Slack-Signature
		},
	}

	// Example slash command request
	b := []byte("text=hello&user_id=U12345678&team_id=T12345678&command=/test")

	// This should fail because the X-Slack-Signature header is missing
	assert.False(t, VerifySlackRequest(r, b))
}

func TestVerifySlackRequestWithInvalidSignatureFormat(t *testing.T) {
	// Random 32-character string
	secret := "2039f48n09c00249u0riunotiu034he9"
	os.Setenv("SLACK_SIGNING_SECRET", secret)

	r := &http.Request{
		Header: http.Header{
			"X-Slack-Request-Timestamp": {"1596411843"},
			// Invalid signature format (missing "v0=" prefix)
			"X-Slack-Signature": {"bf6cccaf6d49158d589bb82e5ef94778d4c6c39bb4ef3a6cc56fe25426c24eb4"},
		},
	}

	// Example slash command request
	b := []byte("text=hello&user_id=U12345678&team_id=T12345678&command=/test")

	// This should fail because the signature format is incorrect (missing "v0=")
	assert.False(t, VerifySlackRequest(r, b))
}



func TestTransformUserReply_BasicReplacement(t *testing.T) {
    // Test Case 1: Basic replacement of "@person" with a formatted user mention.
    // Input: "Howdy, @person! :wave:"
    // Expected Output: "Howdy, <@U12345678>! :wave:"
    assert.Equal(t, "Howdy, <@U12345678>! :wave:", TransformUserReply("Howdy, @person! :wave:", "U12345678"))
}

func TestTransformUserReply_MixedCasePlaceholder(t *testing.T) {
    // Test Case 2: Placeholder with mixed case ("@person") should not be replaced.
    // Input: "Hello, @person! How are you?"
    // Expected Output: "Hello, <@U12345678>! How are you?"
    assert.Equal(t, "Hello, <@U12345678>! How are you?", TransformUserReply("Hello, @person! How are you?", "U12345678"))
}

func TestTransformUserReply_Placeholders(t *testing.T) {
    // Test Case 3: Two Placeholder 
    // Input: "Good morning, @person! Have a nice day @person."
    // Expected Output: "Good morning, <@U12345678>! Have a nice day <@U12345678>."
    assert.Equal(t, "Good morning, <@U12345678>! Have a nice day <@U12345678>.", TransformUserReply("Good morning, @person! Have a nice day @person.", "U12345678"))
}

func TestTransformUserReply_onlyplaceholder(t *testing.T) {
    // Test Case 4: only placeholder
    // Input: "@person"
    // Expected Output: "<@U12345678>"
    assert.Equal(t, "<@U12345678>", TransformUserReply("@person", "U12345678"))
}

func TestTransformUserReply_EmptyInput(t *testing.T) {
    // Test Case 5: Empty input string should return an empty string, as no transformation is needed.
    // Input: ""
    // Expected Output: ""
    assert.Equal(t, "", TransformUserReply("", "U12345678"))
}

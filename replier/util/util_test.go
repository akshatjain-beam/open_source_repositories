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


func TestIsInArray(t *testing.T) {
	assert.True(t, IsInArray([]string{"i", "like", "go", "!"}, "go"))
	assert.False(t, IsInArray([]string{"i", "like", "go", "!"}, "rust"))
}

func TestTransformUserReply(t *testing.T) {
	assert.Equal(t, "Howdy, <@U12345678>! :wave:", TransformUserReply("Howdy, @person! :wave:", "U12345678"))
}

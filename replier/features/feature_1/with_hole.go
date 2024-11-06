package util

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"net/http"
	"os"
	"strings"

	"github.com/cjdenio/replier/db"
	"github.com/slack-go/slack"
)

// HeaderBlock represents a Slack header block
type HeaderBlock struct {
	Type string                 `json:"type"`
	Text *slack.TextBlockObject `json:"text"`
}

// BlockType gets the block's type
func (b HeaderBlock) BlockType() slack.MessageBlockType {
	return slack.MessageBlockType(b.Type)
}

// SendWelcomeMessage sends the specified user a welcome DM.
func SendWelcomeMessage(teamID, userID string) error {
	installation, err := db.GetInstallation(teamID)
	if err != nil {
		return err
	}

	client := slack.New(installation.Token)

	_, _, err = client.PostMessage(userID, slack.MsgOptionBlocks(
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "Hi there, and welcome to Replier! :wave: I make setting up autoreplies for Slack simple. :robot_face: Let me show you around real quick!", false, false), nil, nil),
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "To get started, head on over to my Home tab. From there you can set up your autoreply message, then turn it on! :sparkles:", false, false), nil, nil),
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "Once you've turned your autoreply on, people will see it when they either DM you or mention you in a group DM/private channel/public channel.", false, false), nil, nil),
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "*By the way*, you can put `@person` in your autoreply message to get it replaced by the name of the person who messaged you!", false, false), nil, nil),
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "Want to get more advanced? You can set start/end dates to make sure your autoreply automatically turns on and off at the right time! :calendar:", false, false), nil, nil),
		slack.NewSectionBlock(slack.NewTextBlockObject("mrkdwn", "_That's all from me!_ If you run into any issues, or have any feature requests, please feel free to open an issue on the <https://github.com/cjdenio/replier|GitHub repository>!", false, false), nil, nil),
	), slack.MsgOptionText("Welcome to Replier!", false))

	if err != nil {
		return err
	}

	return nil
}


// The `VerifySlackRequest` function validates the authenticity of a Slack request by checking the HMAC
// signature in the request headers, using the signing secret stored in the "SLACK_SIGNING_SECRET" environment
// variable.
//
// Parameters:
// - r: The HTTP request object received from Slack.
// - body: The raw request body as a byte slice.
// Returns:
// - bool: Returns true if the computed HMAC signature matches the "X-Slack-Signature" header, 
//   confirming that the request is legitimate. Returns false otherwise.
//
// This function generates the HMAC signature by combining the value from the "X-Slack-Request-Timestamp" header
// with the request body, formatted as "v0:<timestamp>:<body>". It then compares this computed signature 
// with the signature provided by Slack, which is prefixed with "v0=".
//
// Note: The function ensures that the data is properly written in the HMAC hash function. If an error occurs 
// during the process, it halts execution and returns false.
$PlaceHolder$

// VerifySlackRequest verifies a Slack request

// IsInArray checks if the value is in the array
func IsInArray(array []string, value string) bool {
	for _, v := range array {
		if v == value {
			return true
		}
	}
	return false
}

// GetUserTimezone gets a Slack user's timezone.
func GetUserTimezone(userID string) (string, error) {
	user, err := db.GetUser(userID)
	if err != nil {
		return "", err
	}

	client := slack.New(user.Token)
	slackUser, err := client.GetUserInfo(user.UserID)
	if err != nil {
		return "", err
	}

	return slackUser.TZ, nil
}

// TransformUserReply transforms a user's reply
func TransformUserReply(reply, userID string) string {
	return strings.ReplaceAll(reply, "@person", fmt.Sprintf("<@%s>", userID))
}

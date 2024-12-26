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

// VerifySlackRequest verifies a Slack request
func VerifySlackRequest(r *http.Request, body []byte) bool {
	mac := hmac.New(sha256.New, []byte(os.Getenv("SLACK_SIGNING_SECRET")))

	body = append([]byte(r.Header.Get("X-Slack-Request-Timestamp")+":"), body...)
	body = append([]byte("v0:"), body...)

	_, err := mac.Write(body)
	if err != nil {
		return false
	}

	return hmac.Equal([]byte("v0="+hex.EncodeToString(mac.Sum(nil))), []byte(r.Header.Get("X-Slack-Signature")))
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
// First Create `IsInArray` function that checks if a given value is present in the provided array of strings.
//
// Parameters:
//   - array ([]string): The array of strings to search through.
//   - value (string): The value to look for in the array.
//
// Returns:
//   - bool: Returns true if the value is found in the array, otherwise false.
//
// Then create `TransformUserReply` that dynamically processes a text input where a placeholder (e.g., @person) needs to be replaced with a properly formatted mention string (<@userID>) for a messaging platform.
	//Note-
	// 1. The placeholder is assumed to be in the exact form @person (not case-insensitive, and no extra characters or numbers).
	// 2. The code must handle multiple instances of the placeholder in the same string replacing them all.
//
// Parameters:
//   reply   string - The input string containing the text to be modified 
//   userID  string - The Slack user ID to be inserted into the user mention format.
//
// Returns:
//   string - The modified string s.
$PlaceHolder$
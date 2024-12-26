package xerrors

import (
	"errors"
	"fmt"
	"regexp"
	"strings"
)

// ValidationError is the custom validation error which stores:
// - OriginType: the struct which gave the error
// - Err: the err to be wrapped by .Error()
type ValidationError struct {
	OriginType string
	OriginName string
	Err        error
}

func (vErr ValidationError) Error() string {
	if vErr.Err == nil {
		return ""
	}
	base := vErr.OriginType + " validation error: " + vErr.Err.Error()
	if vErr.OriginName != "" {
		base += fmt.Sprintf(". At %v", vErr.OriginName)
	}
	return strings.TrimSpace(base)
}

// Create a `fullVErrRegex` which is the regular expression, which matches strings with validation error: , followed by any number of characters (which are captured in groups), and ending with At.
//Create a `tinyVErrRegex` which is the regular expression, which matches strings with validation error: , followed by any number of characters (which are captured in groups)
//
// Than Create `UnwrapValidationError` function that takes an error, checks if it's a validation error, 
// and extracts a clean message from it. If the error is nil or 
// contains no message, it returns nil. If the error string contains 
// the substring ". At", it uses a regex pattern tailored for full validation errors; 
// otherwise, it applies a regex pattern for smaller errors. The function trims 
// any leading "validation error: " and trailing ". At" from the extracted message 
// before returning it as a new error.
  
// Parameters:
//   vErr (error): The error to be unwrapped. If it's nil or its message is empty, 
//   nil is returned.

// Returns:
//   error: A new error with the extracted validation message, or nil if the input 
//   error is empty or nil.
$PlaceHolder$
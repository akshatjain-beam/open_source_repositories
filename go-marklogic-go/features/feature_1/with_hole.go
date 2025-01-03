package testHelper

import (
	"regexp"
	"strings"
)

// Create `NormalizeSpace` function that normalizes the whitespace and formatting in a given string.
//
// This function performs the following steps to clean up and normalize the input string:
// 1. Replaces all consecutive whitespace characters (spaces, tabs, newlines, etc.) with a single space.
// 2. Removes any unnecessary spaces around structural characters like {, }, [, ], :, ,, and ".
// 3. Ensures that there is no extra space between the structural characters (like : and ,) and the values or other structural characters. Specifically:
//    - It removes spaces after commas and colons, ensuring that there is no space between the structural character and the next key name or value.
//    - It preserves spaces before colons, maintaining a single space between the key and the colon in key-value pairs.
// 4. Trims leading and trailing spaces from the final string.
//
// This function is typically useful for cleaning up and normalizing JSON-like strings or any other strings with
// similar formatting requirements.
//
// Parameters:
//   - str (string): The input string that needs to be normalized.
//
// Returns:
//   - string: A new string with normalized whitespace and proper formatting.
$PlaceHolder$


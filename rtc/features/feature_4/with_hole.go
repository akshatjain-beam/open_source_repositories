/*
Package name contains the naming conventions on rtc
*/
package name

import (
	"regexp"
	"strings"
)

// Parenthize puts the string between parenthesis.
// Notice it's a little macro for removing noise on sql queries
func Parenthize(s string) string {
	return `(` + s + `)`
}

// ToSnakeCase returns the string snake_cased
func ToSnakeCase(s string) string {
	return ToDelimitedLowerCase(s, '_')
}

func isUpper(r rune) bool {
	return (r >= 'A' && r <= 'Z')
}

func isLower(r rune) bool {
	return (r >= 'a' && r <= 'z')
}

func isDelimiter(r rune) bool {
	return (r == ' ' || r == '_' || r == '-')
}

// ToDelimitedLowerCase returns the given string lowercased and delimited by the given del
func ToDelimitedLowerCase(s string, del rune) string {
	s = addWordBoundariesToNumbers(s)
	letters := []rune(strings.Trim(s, " "))
	var n []rune
	for i, letter := range letters {
		// treat acronyms as words, eg for JSONData -> JSON is a whole word
		nextCaseIsChanged := false
		if i+1 < len(letters) {
			next := letters[i+1]
			if (isUpper(letter) && isLower(next)) || (isLower(letter) && isUpper(next)) {
				nextCaseIsChanged = true
			}
		}
		if i > 0 && n[len(n)-1] != del && nextCaseIsChanged {
			if isUpper(letter) {
				n = append(n, del)
				n = append(n, letter)
			} else if isLower(letter) {
				n = append(n, letter)
				n = append(n, del)
			}
		} else if isDelimiter(letter) {
			// replace spaces/underscores with delimiters
			n = append(n, del)
		} else {
			n = append(n, letter)
		}
	}
	newString := string(n)
	newString = strings.ToLower(newString)
	return newString
}

// create a function `ToCamelCase` converts a given string to CamelCase format.
//
// This function takes a string and converts it to CamelCase. It first applies the 
// `addWordBoundariesToNumbers` function to ensure numbers and letters are properly 
// separated. Then, it processes the string, capitalizing the first letter of each word 
// (after non-alphanumeric characters like spaces, underscores, and hyphens) while 
// keeping the rest of the letters in lowercase. The result is returned in CamelCase format, 
// where the first letter of each word is capitalized, and there are no spaces, underscores, 
// or hyphens between words.
//
// Parameters:
//   - s: A string containing words and/or numbers to be converted to CamelCase.
//
// Returns:
//   - A string in CamelCase format.
$PlaceHolder$

var numberSequence = regexp.MustCompile(`([a-zA-Z])(\d+)([a-zA-Z]?)`)
var numberReplacement = []byte(`$1 $2 $3`)

func addWordBoundariesToNumbers(s string) string {
	b := []byte(s)
	b = numberSequence.ReplaceAll(b, numberReplacement)
	return string(b)
}

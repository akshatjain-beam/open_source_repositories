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
//  This block handles how delimiters are added to the string depending on the case of the current letter.
//
// - When a case transition is detected (i.e., from uppercase to lowercase or vice versa),
//   a delimiter is inserted to separate the words. This transition is determined by comparing
//   the current letter with the next letter 
	// - If the current letter is uppercase and a case transition is detected,
	//   the delimiter is inserted before the current letter, then the uppercase letter is added to the result.
	// - If the current letter is lowercase  and a case transition is detected,
	//   the lowercase letter is added first, followed by the delimiter. 
// - Ensures that delimiters are not added at the start 
//   of the string or consecutively after another delimiter, maintaining clean word boundaries.
//
// - If the character is a delimiter (space, underscore, etc.), it is replaced by the 
//   specified delimiter.
// - Otherwise, the character is added as-is to the result.
// Note- isUpper(), isLower() and isDelimiter() functions are used to find whether the character is uppercase, lowercase or delimiter respectively.
$PlaceHolder$
	}
	newString := string(n)
	newString = strings.ToLower(newString)
	return newString
}

// ToCamelCase returns the string in CamelCase
func ToCamelCase(s string) string {
	s = addWordBoundariesToNumbers(s)
	s = strings.Trim(s, " ")
	n := ""
	capNext := true
	for _, v := range s {
		if v >= 'A' && v <= 'Z' {
			n += string(v)
		}
		if v >= '0' && v <= '9' {
			n += string(v)
		}
		if v >= 'a' && v <= 'z' {
			if capNext {
				n += strings.ToUpper(string(v))
			} else {
				n += string(v)
			}
		}
		if v == '_' || v == ' ' || v == '-' {
			capNext = true
		} else {
			capNext = false
		}
	}
	return n
}

var numberSequence = regexp.MustCompile(`([a-zA-Z])(\d+)([a-zA-Z]?)`)
var numberReplacement = []byte(`$1 $2 $3`)

func addWordBoundariesToNumbers(s string) string {
	b := []byte(s)
	b = numberSequence.ReplaceAll(b, numberReplacement)
	return string(b)
}

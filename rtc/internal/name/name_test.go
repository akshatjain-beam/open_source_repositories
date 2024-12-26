package name

import "testing"


// Test_ToDelimitedLowerCase tests the ToDelimitedLowerCase function to ensure that
// it correctly converts various input strings into lowercase with words delimited
// by underscores, handling different cases, spacing, and punctuation correctly.
func Test_ToDelimitedLowerCase(t *testing.T) {
	// Define a set of test cases with input strings and their expected output
	cases := [][]string{
		// Test cases where the input string has a mixed case and spaces.
		{"testCase", "test_case"},           // CamelCase to snake_case
		{"TestCase", "test_case"},           // UpperCamelCase to snake_case
		{"Test Case", "test_case"},          // Space-separated words to snake_case
		{" Test Case", "test_case"},         // Leading space should be removed
		{"Test Case ", "test_case"},         // Trailing space should be removed
		{" Test Case ", "test_case"},        // Leading and trailing spaces should be removed
		{"test", "test"},                   // Single lowercase word should remain unchanged
		{"test_case", "test_case"},          // Already in snake_case format
		{"Test", "test"},                   // Single capitalized word to lowercase
		{"", ""},                           // Empty string should return an empty string
		{"ManyManyWords", "many_many_words"}, // CamelCase with multiple words
		{"manyManyWords", "many_many_words"}, // camelCase with multiple words
		{"AnyKind of_string", "any_kind_of_string"}, // Mixed camelCase and space
		{"numbers2and55with000", "numbers_2_and_55_with_000"}, // Numbers mixed with words
		{"JSONData", "json_data"},           // CamelCase with acronym
		{"userID", "user_id"},               // Mixed case with acronym
		{"userIDs", "user_i_ds"},            // Plural with acronym and camelCase
		{"AAAbbb", "aa_abbb"},               // Mixed uppercase and lowercase letters
	}

	// Iterate through the test cases
	for _, i := range cases {
		in := i[0]  // Input string
		out := i[1] // Expected output

		// Call the function with the input string and compare the result to the expected output
		result := ToDelimitedLowerCase(in, '_')
		if result != out {
			// If the result doesn't match the expected output, report an error
			t.Error("'" + in + "'('" + result + "' != '" + out + "')")
		}
	}
}

func TestToCamel(t *testing.T) {
	cases := [][]string{
		// Test 1: A string with an underscore separating two words
		{
			// Input: "test_case"
			// The expected output is "TestCase", where the underscore is removed 
			// and both words are capitalized properly (following CamelCase rules).
			"test_case", "TestCase",
		},
		// Test 2: A string with a single word in lowercase
		{
			// Input: "test"
			// The expected output is "Test". Since the string contains only one word,
			// it should be capitalized as the first letter in CamelCase format.
			"test", "Test",
		},
		// Test 3: A string that is already in CamelCase
		{
			// Input: "TestCase"
			// The expected output is "TestCase". The input is already in CamelCase, 
			// so no changes should be made.
			"TestCase", "TestCase",
		},
		// Test 4: A string with leading and trailing spaces
		{
			// Input: " test  case "
			// The expected output is "TestCase". The extra spaces at the beginning 
			// and end should be removed, and the string should be capitalized in 
			// CamelCase.
			" test  case ", "TestCase",
		},
		// Test 5: An empty string
		{
			// Input: ""
			// The expected output is an empty string. There is no content to convert.
			// The function should handle this edge case gracefully.
			"", "",
		},
		// Test 6: A string with multiple words separated by underscores
		{
			// Input: "many_many_words"
			// The expected output is "ManyManyWords". The underscores are removed, 
			// and each word after the first one is capitalized.
			"many_many_words", "ManyManyWords",
		},
		// Test 7: A string with mixed spaces and underscores
		{
			// Input: "AnyKind of_string"
			// The expected output is "AnyKindOfString". Spaces and underscores are 
			// treated as word separators, and the string is converted to CamelCase 
			// by capitalizing the first letter of each word (except the first one).
			"AnyKind of_string", "AnyKindOfString",
		},
		// Test 8: A string with a hyphen between words
		{
			// Input: "odd-fix"
			// The expected output is "OddFix". The hyphen is treated as a word separator, 
			// and the first letter of each word is capitalized.
			"odd-fix", "OddFix",
		},
		// Test 9: A string with numbers interspersed between words
		{
			// Input: "numbers2And55with000"
			// The expected output is "Numbers2And55With000". The numbers should remain 
			// intact, and the letters surrounding them should be properly capitalized.
			"numbers2And55with000", "Numbers2And55With000",
		},
	}

	// Loop through each test case
	for _, i := range cases {
		in := i[0]
		out := i[1]
		result := ToCamelCase(in)

		// If the result does not match the expected output, log an error
		if result != out {
			t.Error("'" + result + "' != '" + out + "'")
		}
	}
}

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
		{"test_case", "TestCase"},
		{"test", "Test"},
		{"TestCase", "TestCase"},
		{" test  case ", "TestCase"},
		{"", ""},
		{"many_many_words", "ManyManyWords"},
		{"AnyKind of_string", "AnyKindOfString"},
		{"odd-fix", "OddFix"},
		{"numbers2And55with000", "Numbers2And55With000"},
	}
	for _, i := range cases {
		in := i[0]
		out := i[1]
		result := ToCamelCase(in)
		if result != out {
			t.Error("'" + result + "' != '" + out + "'")
		}
	}
}

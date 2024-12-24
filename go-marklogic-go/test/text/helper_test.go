package text

import (
	"testing"
)

func TestNormalizeSpace(t *testing.T) {
	tests := []struct {
		input  string
		output string
	}{
		{
			// Case 1: Test input with spaces around colons and commas. 
			// We want to normalize spaces so that there's space before and no space after colons.
			input:  `{"key" : "value" , "anotherKey" : "anotherValue" ,}`,
			output: `{"key" :"value","anotherKey" :"anotherValue",}`,
		},
		{
			// Case 2: Test input with excessive spaces around colons and commas.
			// We want to ensure all unnecessary spaces are removed to standardize the formatting according to prompt.
			input:  `{"key"    :    "value"   ,    "another" :    "item"   }`,
			output: `{"key" :"value","another" :"item"}`,
		},
		{
			// Case 3: Test input with only before extra spaces. 
			// This should remain unchanged since there are no unnecessary spaces to remove, as all spaces are before colon.
			input:  `{"key" :"value","another" :"item"}`,
			output: `{"key" :"value","another" :"item"}`,
		},
		{
			// Case 4: Test input with multiple key-value pairs and extra spaces.
			// This test ensures that all the key-value pairs are normalized correctly.
			input:  `{"key" : "value" , "another" : "item" , "more" : "data" }`,
			output: `{"key" :"value","another" :"item","more" :"data"}`,
		},
		{
			// Case 5: Test input with varying amounts of spaces between the key-value pairs.
			// We want to ensure that the spaces are normalized, and the result is compact and consistent.
			input:  `{"key" :            "value"         , "more"      :        "data" }`,
			output: `{"key" :"value","more" :"data"}`,
		},
	}

	for _, tt := range tests {
		t.Run(tt.input, func(t *testing.T) {
			got := NormalizeSpace(tt.input)
			if got != tt.output {
				t.Errorf("NormalizeSpace(%q) = %q; want %q", tt.input, got, tt.output)
			}
		})
	}
}

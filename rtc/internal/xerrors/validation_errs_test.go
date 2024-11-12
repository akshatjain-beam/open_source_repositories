package xerrors

import (
	"errors"
	"reflect"
	"testing"
)

func TestValidationError_Error(t *testing.T) {
	type fields struct {
		OriginType string
		OriginName string
		Err        error
	}
	tests := []struct {
		name   string
		fields fields
		want   string
	}{
		{
			name:   "WRAPs CORRECTly a FULLFILLed validationError",
			fields: fields{OriginType: "foo", OriginName: "bar", Err: errBaz},
			want:   "foo validation error: baz. At bar",
		},
		{
			name:   "SKIP ORIGIN information from UNFILLED validationError",
			fields: fields{Err: errBaz},
			want:   "validation error: baz",
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			vErr := &ValidationError{
				OriginType: tt.fields.OriginType,
				OriginName: tt.fields.OriginName,
				Err:        tt.fields.Err,
			}
			if got := vErr.Error(); got != tt.want {
				t.Errorf("ValidationError.Error() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestValidationError_Unwrap(t *testing.T) {
	type fields struct {
		OriginType string
		OriginName string
		Err        error
	}
	tests := []struct {
		name    string
		fields  fields
		wantErr error
	}{
		{
			name:    "err is nil",
			fields:  fields{Err: nil},
			wantErr: nil,
		},
		{
			name:    "SKIP ORIGIN information from UNFILLED validationError",
			fields:  fields{Err: errors.New("baz")},
			wantErr: errBaz,
		},
		{
			name:    "UNWRAPs CORRECTly a FULLFILLed validationError",
			fields:  fields{OriginType: "foo", OriginName: "bar", Err: errBaz},
			wantErr: errBaz,
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			vErr := ValidationError{
				OriginType: tt.fields.OriginType,
				OriginName: tt.fields.OriginName,
				Err:        tt.fields.Err,
			}
			if err := UnwrapValidationError(errors.New(vErr.Error())); !reflect.DeepEqual(err, tt.wantErr) {
				t.Errorf("ValidationError.Unwrap() error = %v, wantErr %v.", err, tt.wantErr)
			}
		})
	}
}
func TestFullVErrRegex(t *testing.T) {
	testCases := []struct {
		// name describes the specific scenario being tested
		name string
		// input is the complete validation error string to be parsed
		input string
		// expected is the error message that should be extracted
		expected string
	}{
		{
			// Tests the basic case where we have a simple error message followed by
			// position information. The regex should extract only the error message
			// part, stopping at the first ". At" occurrence.
			name:     "Valid error with multiple parts and 'At' in the middle",
			input:    "validation error: Missing required field. At line 42",
			expected: "Missing required field",
		},
		{
			// Tests error messages where the word 'empty' appears immediately before
			// the position information. This case ensures the regex correctly handles
			// error messages that end with different words before the ". At" boundary.
			name:     "Valid error with 'At' at the end of description",
			input:    "validation error: Field 'username' cannot be empty. At position 10",
			expected: "Field 'username' cannot be empty",
		},
		{
			// Tests the regex's ability to handle longer error messages. This ensures
			// that the regex can properly handle messages of varying lengths and doesn't
			// have any unexpected behavior with longer strings.
			name:     "Valid error with 'At' appearing after a long description",
			input:    "validation error: A very long error description that spans many characters. At the end",
			expected: "A very long error description that spans many characters",
		},
		{
			// Tests a case where there's additional location information after the
			// "At line" segment. The regex should still capture only up to the first
			// ". At" occurrence, ignoring any subsequent location details.
			name:     "Error with 'At' segments, should match up to last 'At'",
			input:    "validation error: Missing field. At line 42 location X",
			expected: "Missing field",
		},
		{
			// Tests error messages that contain additional metadata after the position
			// information. This ensures the regex correctly handles cases where there's
			// trailing information like error codes or additional context.
			name:     "Error with 'At' segments and trailing text",
			input:    "validation error: Invalid email address. At some point error code 1001",
			expected: "Invalid email address",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Extract the error message using the regex
			matches := fullVErrRegex.FindStringSubmatch(tc.input)

			// Verify that we got a match and it contains at least one capturing group
			if len(matches) < 2 {
				t.Errorf("FullVErrRegex failed to capture for input: %s", tc.input)
				return
			}

			// Verify that the captured error message matches the expected one
			if matches[1] != tc.expected {
				t.Errorf("Expected: %s, but got: %s for input: %s", tc.expected, matches[1], tc.input)
			}
		})
	}
}

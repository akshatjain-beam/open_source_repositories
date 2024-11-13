package xerrors

import (
	"errors"
	"reflect"
	"testing"
)
// TestValidationError_Unwrap tests the UnwrapValidationError function by providing various scenarios
// with different error values and verifying that the function correctly unwraps the error message.
func TestValidationErrorUnwrap(t *testing.T) {
	// Define the structure for the test cases
	type fields struct {
		OriginType string
		OriginName string
		Err        error
	}

	// Define the test cases
	tests := []struct {
		name    string
		fields  fields
		wantErr error
	}{
		{
			name:    "err is nil",
			fields:  fields{Err: nil},
			wantErr: nil, // Test case where the input error is nil, so the function should return nil.
		},
		{
			name:    "SKIP ORIGIN information from UNFILLED validationError",
			fields:  fields{Err: errors.New("baz")},
			wantErr: errBaz, // Test case where only the error is provided (without OriginType/OriginName). The error should be returned as-is.
		},
		{
			name:    "UNWRAPs CORRECTly a FULLFILLed validationError",
			fields:  fields{OriginType: "foo", OriginName: "bar", Err: errBaz},
			wantErr: errBaz, // Test case with a fully populated ValidationError (with OriginType and OriginName). The function should return the underlying error `errBaz`.
		},
		{
			name:    "SKIP ORIGIN information from UNFILLED validationError",
			fields:  fields{Err: errors.New("foo")},
			wantErr: errFoo, // Another case where only the error message is provided (without OriginType/OriginName). The function should return the `errFoo` error.
		},
		{
			name:    "UNWRAPs CORRECTly a FULLFILLed validationError",
			fields:  fields{OriginType: "bar", OriginName: "foo", Err: errBar},
			wantErr: errBar, // A case with a fully populated ValidationError. The function should return the underlying error `errBar`.
		},
	}

	// Loop through all the test cases
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create a new ValidationError with the provided test fields
			vErr := ValidationError{
				OriginType: tt.fields.OriginType,
				OriginName: tt.fields.OriginName,
				Err:        tt.fields.Err,
			}

			// Unwrap the error using the function under test
			if err := UnwrapValidationError(errors.New(vErr.Error())); !reflect.DeepEqual(err, tt.wantErr) {
				t.Errorf("ValidationError.Unwrap() error = %v, wantErr %v.", err, tt.wantErr)
			}
		})
	}
}

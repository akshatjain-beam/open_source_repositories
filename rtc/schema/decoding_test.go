package schema

import (
	"testing"

	"github.com/spf13/afero"

	"github.com/sebach1/rtc/internal/test/thelper"

	"github.com/google/go-cmp/cmp"
)

func UnmarshalValidatorsAndReturn(t *testing.T, sch *Schema) *Schema {
	t.Helper()
	err := sch.applyBuiltinValidators()
	if err != nil {
		t.Fatalf("Couldn't unmarshal validators at helper layer: %v", err)
	}
	return sch
}
// TestFromFilename tests the FromFilename function, which reads a schema from a file,
// either from a local filesystem or a remote URL, and decodes it into a Schema object.
// The test case includes various scenarios to ensure correct error handling and schema 
// processing, including edge cases for unsupported file extensions, inconsistent column types, 
// and case-sensitive file extensions.
func TestFromFilename(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name           string
		goldenFilename string
		fake           bool // Fake the goldenFile (w/ empty content)
		want           *Schema
		wantErr        error
	}{
		{
			// "CORRECT USAGE" tests the scenario where a valid `.jsonnet` file is provided.
			// The test ensures that the function correctly decodes the file and applies any validators.
			name:           "CORRECT USAGE",
			goldenFilename: "schemas.jsonnet",
			want:           UnmarshalValidatorsAndReturn(t, gSchemas.Foo.copy(t)),
			wantErr:        nil,
		},
		{
			// "the schema contains a COLUMN WITH INCONSISTENT VALUE TYPE" checks how the function
			// handles schemas with inconsistent column types. This should trigger an error
			// related to invalid column types being detected during the validation phase.
			name:           "the schema contains a COLUMN WITH INCONSISTENT VALUE TYPE", // Ensure err checking in applyBuiltinValidators
			goldenFilename: "inconsistent_schemas.jsonnet",
			wantErr:        errUnallowedColumnType,
		},
		{
			// "the EXT is NOT ALLOWED" tests the case where a file with an unsupported extension
			// (e.g., `.matlab`) is provided. The function should return an error indicating
			// that the extension is not allowed.
			name:           "the EXT is NOT ALLOWED",
			goldenFilename: "schemas.matlab", // Invalid extension
			fake:           true,
			wantErr:        errUnallowedExt,
		},
		{
			// "handle .JSONNET extension" tests the handling of `.JSONNET`, an uppercase extension.
			name:           "handle .JSONNET extension",
			goldenFilename: "schemas.JSONNET", // Capitalized extension
			fake:           false,
			wantErr:        errUnallowedExt, // Expecting error in Solution 1 due to case mismatch
		},
		{
			// "handle .jsonnet extension" tests a valid `.jsonnet` file, ensuring that the file is
			// processed without any errors when the correct file extension is provided.
			name:           "handle .jsonnet extension",
			goldenFilename: "schemas.jsonnet", // Correct extension
			fake:           false,
			wantErr:        nil, // No error expected
		},
	}

	// Loop through the test cases and run each one
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			Fs := afero.NewMemMapFs()
			// Simulate the file system with or without content depending on the test case
			if tt.fake {
				thelper.AddFileToFs(t, tt.goldenFilename, []byte{}, Fs)
			} else {
				thelper.AddFileToFsByName(t, tt.goldenFilename, "foo", Fs)
			}
			got, err := FromFilename(tt.goldenFilename, Fs)
			// Check if the error matches the expected error for this test case
			if err != tt.wantErr {
				t.Errorf("FromFilename() error = %v, wantErr %v", err, tt.wantErr)
			}
			// If no error is expected, compare the resulting schema with the expected one
			if err == nil {
				return
			}
			// Check for schema mismatch if no error occurred
			if diff := cmp.Diff(tt.want, got); diff != "" {
				t.Errorf("FromFilename() mismatch (-want +got): %s", diff)
			}
		})
	}
}

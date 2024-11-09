package xerrors

import (
	"errors"
	"fmt"
	"testing"

	"github.com/google/go-cmp/cmp"
)

var (
	errFoo = errors.New("foo")
	errBar = errors.New("bar")
	errBaz = errors.New("baz")
)

func TestNewMultiErr(t *testing.T) {
	tests := []struct {
		name     string
		errs     []error
		wantMErr MultiErr
	}{
		{
			name:     "multiple normal errs",
			errs:     []error{errFoo, errBar, errBaz},
			wantMErr: MultiErr{errFoo, errBar, errBaz},
		},
		{
			name:     "nil errs",
			errs:     []error{nil, nil, nil},
			wantMErr: MultiErr{},
		},
		{
			name:     "nil and normal errs",
			errs:     []error{nil, errFoo, nil},
			wantMErr: MultiErr{errFoo},
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotMErrs := NewMultiErr(tt.errs...)
			if diff := cmp.Diff(tt.wantMErr.Error(), gotMErrs.Error()); diff != "" {
				t.Errorf("NewMultiErr() = mismatch(-want +got): %s", diff)
			}
		})
	}
}

//
// This function tests various scenarios where the MultiErr.Error() method is used to ensure that errors
// are properly concatenated into a single string with a separator. The test cases cover a range of use cases
// such as multiple errors, nil errors, and edge cases like large numbers of errors and custom separators.
func TestMultiErr_Error(t *testing.T) {
	tests := []struct {
		name string
		errs MultiErr
		want string
	}{
		{
			name: "multiple normal errs",
			errs: []error{errFoo, errBar, errBaz},
			want: errFoo.Error() + ErrorsSeparator + errBar.Error() + ErrorsSeparator + errBaz.Error() + ErrorsSeparator,
			// This test checks that when multiple non-nil errors are provided, they are concatenated correctly
			// with the separator between each error message.
		},
		{
			name: "nil and normal errs",
			errs: []error{nil, errFoo, nil},
			want: fmt.Sprintf("%s%s", errFoo, ErrorsSeparator),
			// This test checks that nil errors are skipped, and only the non-nil errors are included in the result.
			// The separator is still added after the non-nil error.
		},
		{
			name: "nil errs",
			errs: []error{nil, nil, nil},
			want: "",
			// This test verifies that when all errors are nil, the result should be an empty string, 
			// as there are no errors to concatenate.
		},
		{
			name: "large number of errs",
			errs: []error{errFoo, errBar, errBaz, errFoo, errBar, errBaz, errFoo, errBar, errBaz, errFoo},
			want: errFoo.Error() + ErrorsSeparator + errBar.Error() + ErrorsSeparator + errBaz.Error() + ErrorsSeparator +
				errFoo.Error() + ErrorsSeparator + errBar.Error() + ErrorsSeparator + errBaz.Error() + ErrorsSeparator +
				errFoo.Error() + ErrorsSeparator + errBar.Error() + ErrorsSeparator + errBaz.Error() + ErrorsSeparator + errFoo.Error() + ErrorsSeparator,
			// This test checks that a large number of repeated errors are handled correctly, 
			// ensuring that each error message is concatenated with the separator between them.
		},
		{
			name: "custom separator",
			errs: []error{errFoo, errBar, errBaz},
			want: errFoo.Error() + ErrorsSeparator + errBar.Error() + ErrorsSeparator + errBaz.Error() + ErrorsSeparator,
			// This test ensures that the custom separator used in the `ErrorsSeparator` constant is applied 
			// correctly between each error message.
		},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got := tt.errs.Error()
			if diff := cmp.Diff(tt.want, got); diff != "" {
				t.Errorf("MultiErr.Error() = mismatch (-want +got): %s", diff)
			}
		})
	}
}

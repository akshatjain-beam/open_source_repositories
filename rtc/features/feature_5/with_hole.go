package xerrors

// ErrorsSeparator is the expected string to use when stringifiying multiple errors to one
const ErrorsSeparator = "; "

// MultiErr is an error interface with multiple error
// .Error() will retrieve the appended errs separated by ErrorsSeparator
type MultiErr []error

// UnwrapAll acts as a map func over the MultiErr entity, being the map func the proportioned unwrapper
func (errs MultiErr) UnwrapAll(unwrapper func(error) error) (unwrappedErrs []error) {
	for _, err := range errs {
		unwrappedErrs = append(unwrappedErrs, unwrapper(err))
	}
	return
}

// NewMultiErr returns a MultiErr with the given errs
func NewMultiErr(errs ...error) (mErr MultiErr) {
	for _, err := range errs {
		if err == nil {
			continue
		}
		mErr = append(mErr, err)
	}
	return
}

func NewMultiErrFromCh(errCh chan error) (mErr MultiErr) {
	for err := range errCh {
		mErr = append(mErr, err)
	}
	return
}

// create a function `Error` that implements the error interface for the MultiErr type.
//
// The Error method iterates over all errors in the MultiErr slice, concatenating their
// string representations into a single string. Each error message is separated by a
// predefined separator (`ErrorsSeparator`). If any element in the MultiErr is nil,
// it is skipped.
//
// The resulting string provides a summary of all non-nil errors contained within the
// MultiErr, which can be useful for logging or reporting multiple errors in a single
// message.
//
// Returns:
//   - string: A concatenated string of all non-nil error messages, separated by the
//     defined separator.
$PlaceHolder$
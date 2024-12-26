package schema

import (
	"sync"

	"github.com/sebach1/rtc/integrity"
	"github.com/sebach1/rtc/internal/xerrors"
	"github.com/sebach1/rtc/schema/valide"
)

// A Column is the representation of SQL column which defines the structure of the fields that is contains.
type Column struct {
	Name      integrity.ColumnName `json:"name,omitempty"`
	Validator integrity.Validator
	Type      integrity.ValueType `json:"type,omitempty"`
}

func (c *Column) validateSelf(wg *sync.WaitGroup, vErrCh chan<- error) {
	defer wg.Done()

	if c == nil {
		vErrCh <- c.validationErr(errNilColumn)
		return
	}
	if c.Name == "" {
		vErrCh <- c.validationErr(errNilColumnName)
	}
	if c.Type == "" {
		vErrCh <- c.validationErr(errNilColumnType)
	}
}

func (c *Column) validationErr(err error) *xerrors.ValidationError {
	var name string
	if c == nil {
		name = ""
	} else {
		name = string(c.Name)
	}
	return &xerrors.ValidationError{Err: err, OriginType: "column", OriginName: name}
}

// Validate wraps the column validator func and returns its result
func (c *Column) Validate(val interface{}) error {
	if c.Validator == nil || val == nil {
		return nil
	}
	err := c.Validator(val)
	if err != nil {
		return err
	}
	return nil
}

func (c *Column) unaliasType() {
	switch c.Type {
	case "json":
		c.Type = "json.RawMessage"
	case "bytes":
		c.Type = "[]byte"
	}
}
// Create a function `applyBuiltinValidator` that assigns the appropriate built-in validator function
// based on the Column's Type. It checks the Column's Type and sets the 
// corresponding validator from the `valide` package to the Column's Validator field.
// The supported types include "string", "int", "float32", "float64", 
// "json.RawMessage", and "[]byte". If the Column's Type is empty or unrecognized,
// an error is returned.
//
// This method is useful for automatically setting up the right validation logic
// for column values during schema validation.
//
// Parameters:
//   - c (*Column): A pointer to the Column object. 
//
// Returns:
//   - error: Returns an error if the Column's Type is empty or unrecognized.
//     Possible errors are:
//       - `errNilColumnType` if the Column's Type is an empty string.
//       - `errUnallowedColumnType` if the Column's Type is not supported.
//For example:
//    - If the Column's Type is "string", it assigns `valide.String` as the validator.
$PlaceHolder$
// Assigns the appropiated builtin validator (on schema/valide pkg) given the Column.Type
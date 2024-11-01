package validation

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

const (
	bitFieldName = "BitField"
)

func TestBitFieldOfUnsupportedTypeError(t *testing.T) {
	const (
		bitFieldType = "int"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"int\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)

	e.SetFormatName(formatName)

	e.SetWordName(wordName)

	e.SetBitFieldName(bitFieldName)

	assert.Equal(t,
		errorMessage, e.Error(),
	)
}

// TestBitFieldOfUnsupportedTypeErrorMap tests the error message generation for a bit field of unsupported type "map".
func TestBitFieldOfUnsupportedTypeErrorMap(t *testing.T) {
	const (
		bitFieldType = "map"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"map\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)
	e.SetFormatName(formatName)
	e.SetWordName(wordName)
	e.SetBitFieldName(bitFieldName)

	assert.Equal(t, errorMessage, e.Error())
}

// TestBitFieldOfUnsupportedTypeError tests the error message generation for a bit field of unsupported type "int".
func TestBitFieldOfUnsupportedType_Error(t *testing.T) {
	const (
		bitFieldType = "int"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"int\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)
	e.SetFormatName(formatName)
	e.SetWordName(wordName)
	e.SetBitFieldName(bitFieldName)

	assert.Equal(t, errorMessage, e.Error())
}

// TestBitFieldOfUnsupportedTypeErrorBool tests the error message generation for a bit field of unsupported type "float".
func TestBitFieldOfUnsupportedTypeErrorBool(t *testing.T) {
	const (
		bitFieldType = "float"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"float\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)
	e.SetFormatName(formatName)
	e.SetWordName(wordName)
	e.SetBitFieldName(bitFieldName)

	assert.Equal(t, errorMessage, e.Error())
}

// TestBitFieldOfUnsupportedTypeErrorString tests the error message generation for a bit field of unsupported type "string".
func TestBitFieldOfUnsupportedTypeErrorString(t *testing.T) {
	const (
		bitFieldType = "string"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"string\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)
	e.SetFormatName(formatName)
	e.SetWordName(wordName)
	e.SetBitFieldName(bitFieldName)

	assert.Equal(t, errorMessage, e.Error())
}

// TestBitFieldOfUnsupportedTypeErrorSlice tests the error message generation for a bit field of unsupported type "slice".
func TestBitFieldOfUnsupportedTypeErrorSlice(t *testing.T) {
	const (
		bitFieldType = "slice"

		errorMessage = "" +
			"A bit field is represented " +
			"by an exported field of a word-struct " +
			"of type uintN or bool. " +
			"Argument to Marshal points to a format-struct \"Format\" " +
			"nesting a word-struct \"Word\" " +
			"that has a bit field \"BitField\" " +
			"of unsupported type \"slice\"."
	)

	var (
		e BitFieldError
	)

	e = NewBitFieldOfUnsupportedTypeError(bitFieldType)

	e.SetFunctionName(functionName)
	e.SetFormatName(formatName)
	e.SetWordName(wordName)
	e.SetBitFieldName(bitFieldName)

	assert.Equal(t, errorMessage, e.Error())
}

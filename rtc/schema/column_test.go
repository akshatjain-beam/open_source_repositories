package schema

import (
	"fmt"
	"testing"

	"github.com/google/go-cmp/cmp"
	"github.com/sebach1/rtc/integrity"
	"github.com/sebach1/rtc/schema/valide"
)

func TestColumn_Validate(t *testing.T) {
	t.Parallel()
	type fields struct {
		Name      integrity.ColumnName
		Validator integrity.Validator
	}
	type args struct {
		val interface{}
	}
	tests := []struct {
		name     string
		fields   fields
		args     args
		wantsErr bool // Notice wantSErr (errs are not necessarily std due they're wrapped from the col validator)
	}{
		{
			name:     "passes the validation",
			fields:   fields{Validator: valide.String},
			args:     args{val: "anything"},
			wantsErr: false,
		},
		{
			name:     "doesnt passes the validation",
			fields:   fields{Validator: valide.Int},
			args:     args{val: "anything"},
			wantsErr: true,
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			c := &Column{
				Name:      tt.fields.Name,
				Validator: tt.fields.Validator,
			}
			if err := c.Validate(tt.args.val); (err != nil) != tt.wantsErr {
				t.Errorf("Column.Validate() error = %v, wantErr %v", err, tt.wantsErr)
			}
		})
	}
}

func TestColumn_applyBuiltinValidator(t *testing.T) {
	t.Parallel()
	tests := []struct {
		name          string
		Type          integrity.ValueType
		wantValidator integrity.Validator
		wantType      integrity.ValueType
		wantErr       error
	}{
		{
			// Test case for "JSON" type
			// We expect that the "json" type will be mapped to the "json.RawMessage" type
			// and the corresponding validator should be valide.JSON.
			name:          "JSON type",
			Type:          "json",
			wantType:      "json.RawMessage",
			wantValidator: valide.JSON,
			wantErr:       nil,
		},
		{
			// Test case for "BYTES" type
			// The "bytes" type should map to the Go type "[]byte" and use the validator valide.Bytes.
			name:          "BYTES type",
			Type:          "bytes",
			wantType:      "[]byte",
			wantValidator: valide.Bytes,
			wantErr:       nil,
		},
		{
			// Test case for "STRING" type
			// The "string" type should remain a "string" in Go and use the valide.String validator.
			name:          "STR type",
			Type:          "string",
			wantType:      "string",
			wantValidator: valide.String,
			wantErr:       nil,
		},
		{
			// Test case for "INT" type
			// The "int" type should map to Go's "int" and use the valide.Int validator.
			name:          "INT type",
			Type:          "int",
			wantType:      "int",
			wantValidator: valide.Int,
			wantErr:       nil,
		},
		{
			// Test case for "FLOAT32" type
			// The "float32" type should map to Go's "float32" type and use the valide.Float32 validator.
			name:          "FLOAT32 type",
			Type:          "float32",
			wantType:      "float32",
			wantValidator: valide.Float32,
			wantErr:       nil,
		},
		{
			// Test case for "FLOAT64" type
			// The "float64" type should map to Go's "float64" type and use the valide.Float64 validator.
			name:          "FLOAT64 type",
			Type:          "float64",
			wantType:      "float64",
			wantValidator: valide.Float64,
			wantErr:       nil,
		},
		{
			// Test case for an empty or NIL type
			// An empty string or a "nil" type should result in an error (errNilColumnType).
			name:    "NIL type",
			Type:    "",
			wantErr: errNilColumnType,
		},

		{
			// Test case for an invalid type
			// If the type is not recognized (e.g., "invalid"), the function should return
			// an error (errUnallowedColumnType), and the Type should remain unchanged.
			name:     "INVALID type",
			Type:     "invalid",
			wantType: "invalid",
			wantErr:  errUnallowedColumnType,
		},
	}
	for _, tt := range tests {
		tt := tt
		t.Run(tt.name, func(t *testing.T) {
			t.Parallel()
			c := &Column{Type: tt.Type}
			err := c.applyBuiltinValidator()
			if err != tt.wantErr {
				t.Errorf("Column.applyBuiltinValidator() error = %v, wantErr %v", err, tt.wantErr)
			}

			if fmt.Sprintf("%v", c.Validator) != fmt.Sprintf("%v", tt.wantValidator) {
				t.Errorf("Column.applyBuiltinValidator() mismatch VALIdATOR")
			}

			if diff := cmp.Diff(tt.wantType, c.Type); diff != "" {
				t.Errorf("Column.applyBuiltinValidator() mismatch TYPE (-want +got): %s", diff)
			}
		})
	}
}

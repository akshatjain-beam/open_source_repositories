package metadata

import (
	"reflect"
	"testing"
)

func TestMarshal(t *testing.T) {
	tests := []struct {
		name      string
		bitField  bitFieldMetadata
		value     interface{}
		expected  uint64
	}{
		{
			name: "uint8",
			bitField: bitFieldMetadata{
				length: 4,
				offset: 0,
				kind:   reflect.Uint8,
			},
			// Test case: uint8 value 15 (0b00001111) should be marshaled correctly into the bit field.
			// The bit field has a length of 4 and an offset of 0, so the value should be placed in the first 4 bits of the result.
			// The expected result is 0b00001111 (15 in decimal).
			value:    uint8(15), // 0b00001111
			expected: 0b00001111 << 0,
		},
		{
			name: "uint16",
			bitField: bitFieldMetadata{
				length: 8,
				offset: 0,
				kind:   reflect.Uint16,
			},
			// Test case: uint16 value 255 (0b11111111) should be marshaled correctly into the bit field.
			// The bit field has a length of 8 and an offset of 0, so the value should be placed in the first 8 bits of the result.
			// The expected result is 0b11111111 (255 in decimal).
			value:    uint16(255), // 0b11111111
			expected: 0b11111111 << 0,
		},
		{
			name: "uint64",
			bitField: bitFieldMetadata{
				length: 32,
				offset: 0,
				kind:   reflect.Uint64,
			},
			// Test case: uint64 value 4294967295 (0xFFFFFFFF) should be marshaled correctly into the bit field.
			// The bit field has a length of 32 and an offset of 0, so the value should be placed in the first 32 bits of the result.
			// The expected result is 0xFFFFFFFF (4294967295 in decimal).
			value:    uint64(4294967295), // 0xFFFFFFFF
			expected: 0xFFFFFFFF << 0,
		},
		{
			name: "bool",
			bitField: bitFieldMetadata{
				length: 1,
				offset: 0,
				kind:   reflect.Bool,
			},
			// Test case: boolean value true should be marshaled correctly into the bit field as 1.
			// The bit field has a length of 1 and an offset of 0, so the value should be placed in the first bit of the result.
			// The expected result is 0b1 (1 in decimal).
			value:    true,
			expected: 1 << 0,
		},
		{
			name: "uint16 with offset",
			bitField: bitFieldMetadata{
				length: 5,
				offset: 2,
				kind:   reflect.Uint16,
			},
			// Test case: uint16 value 31 (0b00011111) should be marshaled correctly into the bit field with an offset of 2.
			// The bit field has a length of 5 and an offset of 2, so the value should be placed starting from the 3rd bit of the result.
			// The expected result is 0b1111100 (124 in decimal), which is 31 shifted left by 2 bits.
			value:    uint16(31), // 0b00011111
			expected: 31 << 2,    // Shift left by 2 bits, resulting in 0b1111100 (124)
		},
		
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			reflectionValue := reflect.ValueOf(tt.value)
			result := tt.bitField.marshal(reflectionValue)

			if result != tt.expected {
				t.Errorf("expected %b, got %b", tt.expected, result)
			}
		})
	}
}

```
func (m wordMetadata) unmarshal(bytes []byte, reflection reflect.Value) {
	var (
		bitFieldBytes []byte
		i             int
	)

	for i = 0; i < len(m.bitFields); i++ {
		if len(bytes) < wordLengthUpperLimitBytes {
			bitFieldBytes = make([]byte, wordLengthUpperLimitBytes)

			copy(bitFieldBytes[wordLengthUpperLimitBytes-len(bytes):],
				bytes,
			)

		} else {
			bitFieldBytes = bytes
		}

		m.bitFields[i].unmarshal(bitFieldBytes,
			reflection.Field(i),
		)
	}

	return
}
```
```
func (m wordMetadata) unmarshal(bytes []byte, reflection reflect.Value) {
	var (
		bitFieldBytes []byte
		i             int
	)

	if len(bytes) < wordLengthUpperLimitBytes {
		bitFieldBytes = make([]byte, wordLengthUpperLimitBytes)
		copy(bitFieldBytes[wordLengthUpperLimitBytes-len(bytes):], bytes)
	} else {
		bitFieldBytes = bytes
	}

	for i = range m.bitFields {
		m.bitFields[i].unmarshal(
			bitFieldBytes[wordLengthUpperLimitBytes-m.lengthInBytes:],
			reflection.Field(i),
		)
	}

	return
}
```

```
func FromFilename(filename string, Fs afero.Fs) (*Schema, error) {
	var reader io.Reader
	var err error

	if strings.HasPrefix(filename, "https") {
		reader, err = readRemoteFileByHTTPS(filename)
	} else {
		reader, err = readFsFileByName(filename, Fs)
	}

	if err != nil {
		return nil, err
	}

	ext := strings.ToLower(filepath.Ext(filename))
	sch, err := decodeFromReader(reader, ext)
	if err != nil {
		return nil, err
	}

	err = sch.applyBuiltinValidators()
	if err != nil {
		return nil, err
	}

	return sch, nil
}
```

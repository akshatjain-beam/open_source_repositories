```
func FromFilename(filename string, Fs afero.Fs) (*Schema, error) {
	var content io.Reader
	var err error

	if strings.HasPrefix(filename, "https") { // Delegate url protocol scheme validation to net/http
		content, err = readRemoteFileByHTTPS(filename)
	} else {
		content, err = readFsFileByName(filename, Fs)
	}
	if err != nil {
		return nil, err
	}

	sch, err := decodeFromReader(content, filepath.Ext(filename))
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
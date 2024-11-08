package schema

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"path/filepath"
	"strings"

	"github.com/spf13/afero"
	"gopkg.in/yaml.v2"
)

// FromFilename retrieves a schema with the decoded data of the given filename
// Notice that the filename can be a remote url
//Create a function `FromFilename` that loads a schema from a given filename, which can be either a local file path or a remote URL. If the filename starts with "https", it fetches the schema from the URL using readRemoteFileByHTTPS. Otherwise, it reads the schema from the local filesystem using readFsFileByName and the provided afero.Fs.
//The file content is read into an io.Reader and then decoded based on the file extension using decodeFromReader. The decoded schema is validated using applyBuiltinValidators before being returned. Any errors during file access, decoding, or validation are returned to the caller.
//
// Parameters:
//  - filename: A string representing the file name or URL of the schema to be loaded.
//  - Fs: An afero.Fs interface, which represents the filesystem used to read local files (ignored if the filename is a URL).
//
// Returns:
//  - *Schema: A pointer to the decoded Schema object if successful.
//  - error: An error if there was an issue reading the file, decoding the content, or applying the validators.
$PlaceHolder$

func readFsFileByName(filename string, Fs afero.Fs) (io.Reader, error) {
	body, err := afero.ReadFile(Fs, filename)
	if err != nil {
		return nil, err
	}
	return bytes.NewReader(body), nil
}

func readRemoteFileByHTTPS(url string) (io.Reader, error) {
	resp, err := http.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	return resp.Body, nil
}

func decodeFromReader(reader io.Reader, ext string) (*Schema, error) {
	var err error
	sch := &Schema{}
	switch ext {
	case ".json", ".jsonnet": // Notice that jsonnet is for already decoded jsonnet files
		err = json.NewDecoder(reader).Decode(sch)
	case ".yaml":
		err = yaml.NewDecoder(reader).Decode(sch)
	default:
		err = errUnallowedExt
	}
	if err != nil {
		return nil, err
	}
	return sch, nil
}

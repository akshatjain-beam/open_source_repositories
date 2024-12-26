```
		if i > 0 && n[len(n)-1] != del && nextCaseIsChanged {
			if isUpper(letter) {
				n = append(n, del)
				n = append(n, letter)
			} else if isLower(letter) {
				n = append(n, letter)
				n = append(n, del)
			}
		} else if isDelimiter(letter) {
			// replace spaces/underscores with delimiters
			n = append(n, del)
		} else {
			n = append(n, letter)
		}
```

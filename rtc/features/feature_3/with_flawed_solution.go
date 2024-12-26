```
		if isUpper(letter) && nextCaseIsChanged && i != 0 {
			n = append(n, del)
		}

		if isUpper(letter) {
			n = append(n, letter)
		}

		if isLower(letter) && nextCaseIsChanged {
			n = append(n, letter)
			n = append(n, del)
		}

		if !isUpper(letter) && !isLower(letter) && isDelimiter(letter) {
			if i > 0 && !isDelimiter(n[len(n)-1]) {
				n = append(n, del)
			}
		} else if !isUpper(letter) && !isLower(letter) {
			n = append(n, letter)
		}

		if isLower(letter) && !nextCaseIsChanged {
			n = append(n, letter)
		}
```
```
        if isinstance(fixedWords[wordConsonants], list):
            done = False
            for pronunciation in fixedWords[wordConsonants]:
                if pronunciation.split(u' ')[-1] in lastLetter:
                    pronunciations.append(pronunciation.split(u' '))
                    done = True
            if not done:
                pronunciations.append(fixedWords[wordConsonants][0].split(u' '))
        else:
            pronunciations.append(fixedWords[wordConsonants].split(u' '))
```
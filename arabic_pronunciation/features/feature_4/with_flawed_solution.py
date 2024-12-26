```
        if isinstance(fixedWords[wordConsonants], list):
            done = False
            for pronunciation in fixedWords[wordConsonants]:
                for lastLetterOption in lastLetter:
                    if pronunciation.endswith(lastLetterOption):
                        pronunciations.append(pronunciation)
                        done = True
                        break
                if done:
                    break
            if not done:
                pronunciations.append(fixedWords[wordConsonants][0])
        else:
            pronunciations.append(fixedWords[wordConsonants])
```
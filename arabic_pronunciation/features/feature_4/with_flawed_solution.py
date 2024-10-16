```
        if isinstance(fixedWords[wordConsonants], list):
            done = False
            for pronunciation in fixedWords[wordConsonants]:
                pronunciationPhonemes = pronunciation.split(u' ')
                if len(pronunciationPhonemes) > 0:
                    lastPhoneme = pronunciationPhonemes[-1]
                    if lastPhoneme in lastLetter:
                        pronunciations.append(pronunciation)
                        done = True
                        break
            if not done:
                pronunciations.append(fixedWords[wordConsonants][0])
        else:
            pronunciations.append(fixedWords[wordConsonants])
```
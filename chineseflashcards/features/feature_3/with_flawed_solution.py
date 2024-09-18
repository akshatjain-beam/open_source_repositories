```
  if syl == 'r':
    return syl, 5

  if syl[-1].isdigit():
    tone = int(syl[-1])
    syl = syl[:-1]
  else:
    tone = 5  # Default to neutral tone if not specified

  diacritic_syl = diacritic_syl(syl + str(tone))  # Apply diacritics using existing function

  return diacritic_syl, tone
```
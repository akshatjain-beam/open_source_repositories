```
  # The syllable "r" is an edge case that occurs in a few places in CC-CEDICT
  if syl in ('r', 'r5'):
    return 'r', 5

  if syl[-1] in '12345':
    return diacritic_syl(syl), int(syl[-1])
  for i, vowel_group in enumerate(zip(*DIACRITIC_VOWELS)):
    if set(vowel_group) & set(syl):
      return syl, i + 1
  raise ValueError('diacritic_syl_and_tone got unexpected argument : {}'.format(syl))
```
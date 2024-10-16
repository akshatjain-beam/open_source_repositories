import re
from arabic_pronunciation.constants import unambiguousConsonantMap, fixedWords

# modification in isFixedWord2 is just to return the pronunciations without the word
def isFixedWord2(word):
    pronunciations = []
    lastLetter = ''
    if len(word) > 0:
        lastLetter = word[-1]
    if lastLetter == u'a':
        lastLetter = [u'a', u'A']
    elif lastLetter == u'A':
        lastLetter = [u'aa']
    elif lastLetter == u'u':
        lastLetter = [u'u0']
    elif lastLetter == u'i':
        lastLetter = [u'i0']
    elif lastLetter in unambiguousConsonantMap:
        lastLetter = [unambiguousConsonantMap[lastLetter]]
    wordConsonants = re.sub(u'[^h*Ahn\'>wl}kmyTtfdb]', u'', word)  # Remove all dacritics from word
    if wordConsonants in fixedWords:  # check if word is in the fixed word lookup table
        """
        write line of code that performs as follows-
        - If the pronunciation for the word consonants is a list,`done` is set to False and  it iterates through the list to find a matching pronunciation based on the last letter.
        - If a match is found, the pronunciation is added to the `pronunciations` list and `done` is changed  to True.
        - If no match is found, the first pronunciation in the list is added to the `pronunciations` list.
        - If the pronunciation for the word consonants is not a list, the function simply adds the pronunciation to the `pronunciations` list.

        Note:
            -The `.split(u' ')` method is used to split the pronunciation strings into lists of phonemes.
        """
        $PlaceHolder$
    return pronunciations
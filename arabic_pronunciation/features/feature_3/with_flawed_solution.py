```
def keep_only_arabic(text):
    """
    Create a function `keep_only_arabic` which filter and retain only Arabic words from the input text.

    This function processes an input string line by line, removing any words that are not Arabic. 
    It uses the `is_arabic` method from the `AlphabetDetector` class to identify Arabic words. 
    Only words that are detected as Arabic and consist solely of alphabetic characters are retained. 
    Lines without any Arabic words are returned as empty strings. Consider the removal of last extra new line
    in input text if present.

    Args:
        text (str): The input text containing multiple lines, which may include 
                     Arabic and non-Arabic words.

    Returns:
        str: A string with only Arabic words from the input text, formatted 
            line by line corresponding to the original input. 
    """
    ad = AlphabetDetector()
    result = []
    for line in text.splitlines():
        arabic_words = [word for word in line.split() if ad.is_arabic(word) and word.isalpha()]
        result.append(' '.join(arabic_words))
    return '\n'.join(result).strip()
```
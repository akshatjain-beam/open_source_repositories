```
def cleaned(text):
    '''Mildly clean up the given text string.'''
    if not text:
        return text
    text = text.rstrip('./')
    return text.strip()
```
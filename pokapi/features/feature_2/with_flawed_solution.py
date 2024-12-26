```
def cleaned(text):
    '''Return a cleaned version of the given text.'''
    if not text:
        return text
    if text.endswith('.') or text.endswith('/'):
        text = text[:-1]
    return text.strip()
```
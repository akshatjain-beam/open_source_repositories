```
def remove_links(text):
    # return re.sub(r'\s*(?:https?://)?www\.\S*\.[A-Za-z]{2,5}\s*', ' ', text, flags=re.MULTILINE).strip()
    # return re.sub(r'^https?:\/\/.*[\r\n]*', '', clean_text, flags=re.MULTILINE)
    return re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', text, flags=re.MULTILINE)
```
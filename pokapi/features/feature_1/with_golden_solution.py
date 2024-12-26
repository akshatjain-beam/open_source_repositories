```
    def extracted_name(field):
        author = field['name']
        
        matched = regex.match(r'[-.,\p{L} ]+', author)
        if matched:
            return matched.group().strip(' ,')
        else:
            return author
```
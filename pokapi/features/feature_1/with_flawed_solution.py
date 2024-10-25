```
    def extracted_name(field):
        return regex.match(r'^[-\.\,\p{L}\s]*(.*?)[,-\s]*$', field['name']).group(1)
```
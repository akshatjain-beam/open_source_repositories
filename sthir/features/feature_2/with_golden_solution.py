```
    string_length = len(string)

    # If drop remaining is True, trim the string
    if drop_remaining and string_length % chunk_size != 0:
        closest_multiple = string_length - string_length % chunk_size
        string = string[:closest_multiple]

    for c in range(0, len(string), chunk_size):
        yield string[c:c + chunk_size]
```
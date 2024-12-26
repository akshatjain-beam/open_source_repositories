```
def split_regions(text):
    res = []
    current_prefix = None
    current_text = ""
    current_region = None
    for line in text.splitlines(keepends=False):
        prefix = get_prefix(line)
        if prefix != current_prefix:
            current_region = Region(text=line + "\n", prefix=prefix)
            res.append(current_region)
            current_prefix = prefix
        else:
            current_region.text += line + "\n"
    return res
```
```
def split_regions(text):
    regions = []
    current_region = None

    for line in text.splitlines(keepends=True):
        prefix = get_prefix(line)
        if prefix == current_region.prefix if current_region else None:
            current_region.text += line
        else:
            if current_region:
                regions.append(current_region)
            current_region = Region(text=line, prefix=prefix)
    if current_region:
        regions.append(current_region)
    return regions
```
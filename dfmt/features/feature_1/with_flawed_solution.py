```
def split_regions(text):
    regions = []
    current_region = None
    for line in text.splitlines(keepends=True):
        new_prefix = get_prefix(line)
        if current_region is not None and current_region.prefix == new_prefix:
            current_region.text += line
        else:
            current_region = Region(text=line, prefix=new_prefix)
            regions.append(current_region)
    return regions
```
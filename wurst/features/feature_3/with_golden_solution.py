```
def convert_to_location_dictionary(array, locations=REGIONS):
    """Convert array of values ``array`` with order ``locations`` to a dictionary:

        {
            'place name': value
        }

    Assumes that the first axis of the array matches the locations."""
    size = array.shape[0]
    if len(array.shape) == 1:
        return {
            loc: array[index] for index, loc in enumerate(locations) if index < size
        }
    else:
        return {
            loc: array[index, ...]
            for index, loc in enumerate(locations)
            if index < size
        }
```
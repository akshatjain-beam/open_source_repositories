```
def convert_to_location_dictionary(array, locations=REGIONS):
    return {location: array[i] for i, location in enumerate(locations)}
```
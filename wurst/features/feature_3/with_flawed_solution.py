```
def convert_to_location_dictionary(array, locations=REGIONS):
    """Convert a array of values to a dictionary with location names as keys.

    Parameters:
    - array (numpy.ndarray): numpy array containing values to be associated with the locations.
    - locations (list, optional): List of location names. Defaults to REGIONS.

    Returns:
    - dict: A dictionary with location names as keys and corresponding values.

    Notes:
    - The function assumes that the first axis of the input array matches the order of locations.
    - If the input array is 1D, the function returns a dictionary with scalar values.
    - If the input array is 2D or higher, the function returns a dictionary with array values.
    - If the length of the `array` is less than the length of `locations`, only the corresponding 
      values for the available locations will be included in the output dictionary.
    """
    return {location: value for location, value in zip(locations, array)}
```
from . import REGIONS


def relative_change(dataset, years, start, end):
    """Calculate fractional change values from year ``start`` to year ``end``.

    Assumes years are the last axis of the array. Normalizes by the starting value."""
    years = list(years)
    return (
        dataset[..., years.index(end)] - dataset[..., years.index(start)]
    ) / dataset[..., years.index(start)]


"""
write a function `convert_to_location_dictionary` that will
Convert a 1D or 2D array of values to a dictionary with location names as keys.

Parameters:
- array (numpy.ndarray): numpy array containing values to be associated with the locations.
- locations (list, optional): List of location names. Defaults to REGIONS.

Returns:
- dict: A dictionary with location names as keys and corresponding values.

Notes:
- The function assumes that the first axis of the input array matches the order of locations.
- If the input array is 1D, the function returns a dictionary with scalar values.
- If the input array is 2D or higher, the function returns a dictionary with array values.
"""
$PlaceHolder$

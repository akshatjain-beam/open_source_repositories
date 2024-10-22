

from .metadata import REGIONS


def relative_change(dataset, years, start, end):
    """
    Calculate fractional change values from year start to year end.
    The change is calculated as (value at end - value at start) / value at start.
    Assumes years are the last axis of the array.

    Parameters:
    - dataset (numpy.ndarray): A NumPy array where the last axis represents different years.
    - years (iterable): An iterable containing the years corresponding to the last axis of `dataset`.
    - start (int or float): The starting year for calculating the relative change.
    - end (int or float): The ending year for calculating the relative change.

    Returns:
    - numpy.ndarray: An array of the same shape as `dataset` but with the last axis reduced, containing the fractional change values from the year `start` to the year `end`.
    """
    $PlaceHolder$
    


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

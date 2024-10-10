```
@lru_cache(maxsize=5570 * 2)
def split_state_city(text):
    """
    Split a string into state and city.

    1. Checks if the first part of the string is a two-letter state acronym.
       - If true, returns the acronym and the remaining string as the city name.
    2. If the first part is not a state acronym, it assumes the string begins with a full state name.
       - Iteratively joins words to form possible state names.
       - Checks against a predefined dictionary of state names (STATE_NAMES).
       - Once found, returns the full state name and the remaining part of the string as the city name.

    Notes:
        The function raises a ValueError if the input string does not contain a recognizable state name or acronym.
        This function relies on an external `slug` function to normalize the state name.
        The function uses `functools.lru_cache` to cache results for frequently requested combinations with max size of `5570*2`.

    Args:
        text (str): name of the state and city.

    Returns:
        tuple: containing the state and city.
    
    Raises:
        ValueError: If the input does not contain a recognizable state name or acronym.
    """
    parts = text.split()
    if len(parts) < 2:
        raise ValueError(f"Could not split state and city from: {text!r}")
    if parts[0].upper() in STATE_CODES:
        return parts[0].upper(), " ".join(parts[1:])
    state_parts = [parts[0]]
    for i in range(1, len(parts)):
        possible_state = " ".join(state_parts)
        state_slug = slug(possible_state)
        if state_slug in STATE_NAMES:
            return STATE_NAMES[state_slug], " ".join(parts[i:])
        state_parts.append(parts[i])
    raise ValueError(f"Could not determine state from: {text!r}")
```
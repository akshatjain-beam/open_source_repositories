```
def get_stroke_groups(stroke: str) -> Tuple[str, str, str, str]:
    """Parses a stroke into its logical stroke groups.

    Args:
        stroke: The stroke to create groups from.

    Returns:
        A tuple of the following, all in steno order:
        The keys in the 'initial' group of the stroke.
        The keys in the 'medial' group of the stroke.
        The keys in the 'final' group of the stroke.
        The keys in the 'number' group of the stroke.

    Raises:
        KeyError: The provided stroke was considered invalid.
    """

    result = STROKE_REGEX.match(stroke)
    if not stroke or not result:
        raise KeyError()

    stroke_groups = result.groupdict()
    initial = stroke_groups.get('initial')
    medial = stroke_groups.get('medial')
    final = stroke_groups.get('final', '')
    numbers = (stroke_groups.get('number_start', '')
               + stroke_groups.get('number_end', ''))

    # Pull out the dash from the medial if it exists as it causes
    # problems if caller assumes only valid "keys" are in the string
    medial = medial.replace(STENO_DASH, '')

    return initial, medial, final, numbers
```
```
def lookup(strokes: Tuple[str, ...]) -> str:
    """Retrieves the text output corresponding to the provided strokes.

    Args:
        strokes: A tuple of strokes to look up text for.

    Returns:
        The text text output for the stroke.

    Raises:
        KeyError: The lookup failed to find any matching text.

    Notes:
        If the input strokes are invalid or cannot be parsed, a KeyError is raised.
        The function uses the INITIAL, MEDIAL, and FINAL dictionaries to compose the text output.
        The hgtk library is used to compose the text output into a single Unicode character.
        If any errors occur during the lookup or composition process, a KeyError is raised.
        If length of strokes is not equal to LONGEST_KEY , a KeyError is raised.
    """

    if len(strokes) != LONGEST_KEY:
        raise KeyError()

    initial, medial, final, _ = get_stroke_groups(strokes[0])

    try:
        initial = INITIAL[initial]
        medial = MEDIAL[medial]
        final = FINAL[final]
        return hgtk.letter.compose(initial, medial, final)
    except KeyError:
        raise KeyError()
```
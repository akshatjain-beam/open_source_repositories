```
def lookup(strokes: Tuple[str]) -> str:
    """Gets the text that the provided strokes would output.

    Args:
        strokes: A tuple of strokes to look up text for.

    Returns:
        The text text output for the stroke.

    Raises:
        KeyError: The lookup failed to find any matching text.
    """

    if len(strokes) != LONGEST_KEY:
        raise KeyError()
    initial, medial, final, numbers = get_stroke_groups(strokes[0])

    if numbers:
        raise KeyError()

    try:
        text = f'{INITIAL[initial]}{MEDIAL[medial]}{FINAL[final]}'
        output = hgtk.text.compose(f'{text}{hgtk.text.DEFAULT_COMPOSE_CODE}')
    except Exception:
        raise KeyError()

    return f'{output}{OPERATOR_ATTACH}'
```
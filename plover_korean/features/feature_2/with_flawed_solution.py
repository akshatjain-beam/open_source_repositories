```
def lookup(strokes: Tuple[str, ...]) -> str:
    """
    Retrieves the text output corresponding to the provided strokes.

    Args:
        strokes (Tuple[str]): A tuple of strokes to look up text for.

    Returns:
        str: The text output for the strokes with `OPERATOR_ATTACH` appended.

    Raises:
        KeyError: If the lookup fails to find any matching text.

    Notes:
        - If the length of the strokes tuple is not equal to LONGEST_KEY, a KeyError is raised.
        - The function extracts the initial, medial, final and numbers components using the `get_stroke_groups` function.
        - If any of the strokes contain numbers, a KeyError is raised.
        - The function uses the INITIAL, MEDIAL, and FINAL dictionaries to map the stroke components to text.
        - The hgtk.text library's `DEFAULT_COMPOSE_CODE` is used to compose the final text output.
        - If any errors occur during the lookup or composition process, a KeyError is raised.
    """
    if len(strokes) != LONGEST_KEY:
        raise KeyError("Invalid stroke length")
    if any(char.isdigit() for char in strokes[0]):
        raise KeyError("Strokes cannot contain numbers")
    initial, medial, final, numbers = get_stroke_groups(strokes[0])
    try:
        return hgtk.text.compose(initial, medial, final) + OPERATOR_ATTACH
    except:
        raise KeyError
```
"""Reusable functionality needed throughout the system."""

from typing import Tuple, Callable
import re
"""
Write a Regular expression pattern to match Korean consonant-vowel pairs.

This pattern is designed to match the structure of Korean characters, 
which consist of an initial consonant, a medial vowel, and a final consonant.

The pattern is divided into five groups:

* `number_start`: Matches any of the digits 1-5 (optional)
* `initial`: Matches any of the Korean consonants ㅎ, ㅁ, ㄱ, ㅈ, ㄴ, ㄷ, ㅇ, ㅅ, ㅂ, ㄹ (optional)
* `medial`: Matches any of the Korean vowels ㅗ, ㅏ, ㅜ, \-, *, ㅓ, ㅣ (optional)
* `number_end`: Matches any of the digits 6-9, 0 (optional)
* `final`: Matches any of the Korean consonants ㅎ, ㅇ, ㄹ, ㄱ, ㄷ, ㅂ, ㄴ, ㅅ, ㅈ, ㅁ (optional)
Note:
    The pattern must match the entire string, as indicated by the `^` and `$` anchors.

Example:
     "ㅈㅏ*" -> { 'number_start': '', 'initial': 'ㅈ', 'medial': 'ㅏ*', 'number_end': '', 'final': '' }
"""
$PlaceHolder$
STENO_DASH = '-'


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


def compare_numeric_text(text: str, relate: Callable) -> bool:
    """Compares numeric text with itself sequentially.

    Checks each digit in the numeric string in order, comparing the them
    according to the provided relationship one by one.

    Args:
        text: The numeric text string to check.
        relate: The operator function to compare sequential entries with.

    Returns:
        If the numeric text sequentially follows the provided relationship.
    """

    if not text.isdigit():
        return False

    current = text[0]
    for number in text[1:]:
        if relate(number, current):
            current = number
        else:
            return False

    return True

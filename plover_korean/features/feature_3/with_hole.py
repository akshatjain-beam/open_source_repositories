"""Reusable functionality needed throughout the system."""

from typing import Tuple, Callable
import re


STROKE_REGEX = re.compile(r'''
    ^
    (?P<number_start> [12345]*)
    (?P<initial> [ㅎㅁㄱㅈㄴㄷㅇㅅㅂㄹ]*)
    (?P<medial> [ㅗㅏㅜ\-*ㅓㅣ]*)
    (?P<number_end> [67890]*)
    (?P<final> [ㅎㅇㄹㄱㄷㅂㄴㅅㅈㅁ]*)
    $
    ''', re.VERBOSE)

STENO_DASH = '-'


"""
Create a function `get_stroke_groups` which parses a steno stroke into its logical components.

This function extracts the components of a steno stroke using `STROKE_REGEX` regex, categorizing them into
initial, medial, final, and numeric groups based on a predefined regex pattern.

Args:
    stroke: A string representing the steno stroke to be parsed.

Returns:
    A tuple containing the following components in steno order:
    - initial: The keys in the 'initial' group of the stroke.
    - medial: The keys in the 'medial' group of the stroke.
    - final: The keys in the 'final' group of the stroke (empty string if not present).
    - numbers: The keys in the 'number' group of the stroke (combined from both `number_start` and `number_end`).

Raises:
    KeyError: If the provided stroke is invalid or does not match the expected pattern.

Note:
    - Pull out the dash from the `medial` if it exists

Example:
    >>> get_stroke_groups('STKPWOR')
    ('STKPW', 'OR', '', '')
"""
$PlaceHolder$


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

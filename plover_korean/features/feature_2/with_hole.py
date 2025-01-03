"""Core functionality for the CAS-based Korean stenography system."""

from typing import Tuple, List

import hgtk

from plover_korean.system.cas.util import get_stroke_groups


LONGEST_KEY = 1
OPERATOR_ATTACH = '{^}'

# TODO: Consider adding a combo INITIAL / MEDIAL list for
#       conjunction cases like 그리 = ㄱㄹㅣ and 그러 = ㄱㄹㅓ
#       to make words like 그런, 그릴, etc.
INITIAL = {
    # Base functionality
    'ㄱ': 'ㄱ',
    'ㄱㅇ': 'ㄲ',
    'ㄴ': 'ㄴ',
    'ㄷ': 'ㄷ',
    'ㄷㅇ': 'ㄸ',
    'ㄹ': 'ㄹ',
    'ㅁ': 'ㅁ',
    'ㅂ': 'ㅂ',
    'ㅇㅂ': 'ㅃ',
    'ㅅ': 'ㅅ',
    'ㅇㅅ': 'ㅆ',
    '': 'ㅇ',
    'ㅈ': 'ㅈ',
    'ㅈㅇ': 'ㅉ',
    'ㅎㅈ': 'ㅊ',
    'ㅎㄱ': 'ㅋ',
    'ㅎㄷ': 'ㅌ',
    'ㅎㅂ': 'ㅍ',
    'ㅎ': 'ㅎ'
}

MEDIAL = {
    # Base functionality
    'ㅏ': 'ㅏ',
    'ㅏㅣ': 'ㅐ',
    'ㅏ*': 'ㅑ',
    'ㅏ*ㅓ': 'ㅒ',
    'ㅓ': 'ㅓ',
    'ㅓㅣ': 'ㅔ',
    '*ㅓ': 'ㅕ',
    'ㅗㅓㅣ': 'ㅖ',
    'ㅗ': 'ㅗ',
    'ㅗㅏ': 'ㅘ',
    'ㅗㅏㅣ': 'ㅙ',
    'ㅗㅣ': 'ㅚ',
    'ㅗ*': 'ㅛ',
    'ㅜ': 'ㅜ',
    'ㅜㅓ': 'ㅝ',
    'ㅜㅓㅣ': 'ㅞ',
    'ㅜㅣ': 'ㅟ',
    'ㅜ*': 'ㅠ',
    'ㅏㅓ': 'ㅡ',
    'ㅏㅓㅣ': 'ㅢ',
    'ㅣ': 'ㅣ'
}

FINAL = {
    # Base functionality
    '': '',
    'ㄱ': 'ㄱ',
    'ㅇㄱ': 'ㄲ',
    'ㄱㅅ': 'ㄳ',
    'ㄴ': 'ㄴ',
    'ㄴㅈ': 'ㄵ',
    'ㅎㄴ': 'ㄶ',
    'ㄷ': 'ㄷ',
    'ㄹ': 'ㄹ',
    'ㄹㄱ': 'ㄺ',
    'ㄹㅁ': 'ㄻ',
    'ㄹㅂ': 'ㄼ',
    'ㄹㅅ': 'ㄽ',
    'ㅎㄹㄷ': 'ㄾ',
    'ㅎㄹㅂ': 'ㄿ',
    'ㅎㄹ': 'ㅀ',
    'ㅁ': 'ㅁ',
    'ㅂ': 'ㅂ',
    'ㅂㅅ': 'ㅄ',
    'ㅅ': 'ㅅ',
    'ㅇㅅ': 'ㅆ',
    'ㅇ': 'ㅇ',
    'ㅈ': 'ㅈ',
    'ㅎㅈ': 'ㅊ',
    'ㅎㄱ': 'ㅋ',
    'ㅎㄷ': 'ㅌ',
    'ㅎㅂ': 'ㅍ',
    'ㅎ': 'ㅎ',

    # Conjugations
    'ㄷㄴ': 'ㄴ다',
    'ㅂㄴ': 'ㅂ니다',
    'ㅂㄴㅅㅈ': 'ㅆ습니다',
    'ㄷㅅ': 'ㅆ다',
    'ㅂㄴㅅ': 'ㅂ니까',
    'ㅂㄴㅅㅁ': 'ㅆ습니까',
    'ㄷㅂㅅ': 'ㅂ시다',
    'ㅇㄴ': '운',
    'ㅇㄹ': '울',
    'ㅇㅁ': '움',
    'ㄱㄴ': 'ㄴ가',
    'ㄱㄷㄴ': 'ㄴ다고',
    'ㄱㄴㅈ': 'ㄴ지',
    'ㄹㄷ': 'ㄹ 때',
    # TODO: This conflicts with 닔 type of syllables.
    #       Need to make alternate rule from the theory?
    # 'ㄹㅅ': 'ㄹ 수',
    'ㄹㅈ': 'ㄹ지',
    'ㄹㄱㅁ': 'ㄹ까',
    'ㄷㅂ': 'ㅂ다',
    'ㄱㅂ': 'ㅂ게',
    'ㅂㅅㅈ': 'ㅂ고',
    'ㅂㅈ': 'ㅂ지',
    'ㅂㅈㅁ': 'ㅂ지만',

    # Particles
    # TODO: should they all have automatic spaces
    'ㄱㄷ': '가',
    'ㅅㅈ': '게',
    'ㅇㄹㄱㄷ': '고',
    'ㄷㅈ': '다',
    'ㄴㅅㅈㅁ': '는',
    'ㅎㅇㄹ': '라',
    'ㅇㄹㄱ': '어',
    'ㄹㄴㅅ': '나',
    'ㄴㅅ': '니',
    'ㄴㅅㅈ': '니까',
    'ㄴㅁ': '면',
    'ㄴㅅㅁ': '면서',
    'ㄷㅁ': '도',
    'ㄹㄱㄷ': '도록',
    'ㄱㅈ': '지',
    'ㅈㅁ': '지만',
    'ㅎㄷㅂ': '부터'
}

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
$PlaceHolder$

def reverse_lookup(text: str) -> List[Tuple[str]]:
    """Gets the possible strokes that would result in the provided text.

    Args:
        text: The text to look up strokes for.

    Returns:
        A list of stroke tuples. An empty list will be returned if no possible
        strokes were found.
    """

    output = []

    # TODO: Don't proceed further yet, still in progress.
    #       1ㅎ-ㅇ crashes the suggestions window
    return output

    # Currently, can only look up single syllable block cases
    try:
        initial, medial, final = hgtk.letter.decompose(text)
        stroke = []

        for key, value in INITIAL.items():
            if value == initial:
                for letter in key:
                    stroke.append(f'{letter}-')
                break

        for key, value in MEDIAL.items():
            if value == medial:
                for letter in key:
                    if letter in ['ㅗ', 'ㅏ', 'ㅜ']:
                        stroke.append(f'{letter}-')
                    else:
                        stroke.append(f'-{letter}')
                break

        for key, value in FINAL.items():
            if value == final:
                for letter in key:
                    stroke.append(f'-{letter}')
                break

        output.append((stroke,))
    except:
        output = []

    return output

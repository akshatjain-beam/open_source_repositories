"""Core functionality for the CAS-based Korean stenography system."""

from typing import Tuple, List

import hgtk

from plover_korean.system.cas.util import get_stroke_groups


LONGEST_KEY = 1
OPERATOR_ATTACH = '{^}'

# TODO: Consider adding a combo INITIAL / MEDIAL list for
#       conjunction cases like 그리 = ㄱㄹㅣ and 그러 = ㄱㄹㅓ
#       to make words like 그런, 그릴, etc.
"""
create  Python dictionaries named `INITIAL` and `MEDIAL` that maps Korean consonants and their combinations to their corresponding composed forms. The dictionary should include entries as key and value pairs where keys for `INITIAL` are - ['ㄱ', 'ㄱㅇ', 'ㄴ', 'ㄷ', 'ㄷㅇ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅇㅂ', 'ㅅ', 'ㅇㅅ', '', 'ㅈ', 'ㅈㅇ', 'ㅎㅈ', 'ㅎㄱ', 'ㅎㄷ', 'ㅎㅂ', 'ㅎ']
and `MEDIAL` are ['ㅏ', 'ㅏㅣ', 'ㅏ*', 'ㅏ*ㅓ', 'ㅓ', 'ㅓㅣ', '*ㅓ', 'ㅗㅓㅣ', 'ㅗ', 'ㅗㅏ', 'ㅗㅏㅣ', 'ㅗㅣ', 'ㅗ*', 'ㅜ', 'ㅜㅓ', 'ㅜㅓㅣ', 'ㅜㅣ', 'ㅜ*', 'ㅏㅓ', 'ㅏㅓㅣ', 'ㅣ'].

Example:
>>'': 'ㅇ'
"""
$PlaceHolder$

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

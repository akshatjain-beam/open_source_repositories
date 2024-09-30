import chineseflashcards
import pytest

from chineseflashcards import CedictWord, _parse_line, Classifier


def compare_cedict_words(word1, word2):
    """
    Compare two CedictWord objects for equality.
    This function checks that all attributes of the two CedictWord objects match.
    If the classifiers are present, it compares each classifier as well.
    """
    # List of attributes to compare
    attributes = ['trad', 'simp', 'pinyin', 'tw_pinyin', 'defs']
    clfrs_attributes = ['trad', 'simp', 'pinyin']

    # Check each attribute
    for attr in attributes:
        assert getattr(word1, attr) == getattr(word2, attr), \
            f"{attr} do not match: {getattr(word1, attr)} != {getattr(word2, attr)}"

    # Compare classifiers
    if word1.clfrs is None and word2.clfrs is None:
        pass  # Both are None, so they match
    elif word1.clfrs is None or word2.clfrs is None:
        assert False, f"One of the classifiers is None: {word1.clfrs} != {word2.clfrs}"
    else:
        for clfrs1, clfrs2 in zip(word1.clfrs, word2.clfrs):
            for attr in clfrs_attributes:
                assert getattr(clfrs1, attr) == getattr(clfrs2, attr), \
                    f"{attr} do not match: {getattr(word1, attr)} != {getattr(word2, attr)}"


def test_diacritic_syl_r():
    """
    Test diacritic_syl function with input 'r'.
    It should return 'r' since 'r' does not have a diacritic.
    """
    assert chineseflashcards.diacritic_syl('r') == 'r'


def test_diacritic_syl_and_tone_r():
    """
    Test diacritic_syl_and_tone function with input 'r'.
    It should return a tuple ('r', 5) indicating 'r' without a diacritic and a neutral tone.
    """
    assert chineseflashcards.diacritic_syl_and_tone('r') == ('r', 5)


def test_parse_line_basic():
    """
    Test the _parse_line function with a basic input line.
    The input line contains traditional and simplified characters, pinyin, and definitions.
    It should correctly parse all components and return a CedictWord object.
    """
    line = "AA制 AA制 [A A zhi4] /to split the bill/to go Dutch/"
    expected = CedictWord(
        'AA制',
        'AA制',
        'A A zhi4',
        None,
        ['to split the bill', 'to go Dutch'],
        None
    )
    result = _parse_line(line)
    compare_cedict_words(result, expected)


def test_parse_line_with_taiwanese_pronunciation():
    """
    Test the _parse_line function with an input line that includes a Taiwanese pronunciation.
    The input line contains traditional and simplified characters, pinyin, Taiwanese pronunciation, and definitions.
    It should correctly parse all components and return a CedictWord object.
    """
    line = "你好 nǐhǎo [Chinese] /Taiwan pr. [nǐ hǎo]/hello; hi"
    expected = CedictWord(
        '你好',
        'nǐhǎo',
        'Chinese',
        'nǐ hǎo',
        [],
        None
    )
    result = _parse_line(line)
    compare_cedict_words(result, expected)


def test_parse_line_with_classifiers():
    """
    Test the _parse_line function with an input line that includes classifiers.
    The input line contains traditional and simplified characters, pinyin, classifiers, and definitions.
    It should correctly parse all components, including the classifiers, and return a CedictWord object.
    """
    # line = "你好 nǐhǎo [Chinese] /CL:個,名/hello; hi"
    line = "黨 党 [dang3] /party/association/club/society/CL:個|个[ge4]/"
    expected = CedictWord(
        '黨',
        '党',
        'dang3',
        None,
        ['party', 'association', 'club', 'society'],
        [Classifier.parse('個|个[ge4]')]
    )
    result = _parse_line(line)
    compare_cedict_words(result, expected)


def test_parse_line_with_empty_classifiers():
    """
    Test the _parse_line function with an input line that includes empty classifiers.
    The input line contains traditional and simplified characters, pinyin, empty classifiers, and definitions.
    It should correctly parse all components, including the empty classifiers, and return a CedictWord object.
    """
    line = "你好 nǐhǎo [Chinese] /CL:[]/Taiwan pr. [nǐ hǎo]/hello; hi"
    expected = CedictWord(
        '你好',
        'nǐhǎo',
        'Chinese',
        'nǐ hǎo',
        [],
        []
    )
    result = _parse_line(line)
    compare_cedict_words(result, expected)


def test_parse_line_invalid_format():
    """
    Test the _parse_line function with an invalid input line format.
    The input line does not follow the expected format, so it should raise an AttributeError.
    """
    line = "Invalid line format"
    with pytest.raises(AttributeError):
        _parse_line(line)


def test_parse_line_multiple_categories():
    """
    Test the _parse_line function with an input line that includes multiple categories.
    The input line contains traditional and simplified characters, pinyin, and multiple categories in the definitions.
    It should correctly parse all components and return a CedictWord object.
    """
    line = "ABC ABC [Category1 Category2] /to split the bill/to go Dutch/"
    expected = CedictWord(
        'ABC',
        'ABC',
        'Category1 Category2',
        None,
        ['to split the bill', 'to go Dutch'],
        None
    )
    result = _parse_line(line)
    compare_cedict_words(result, expected)

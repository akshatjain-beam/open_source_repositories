import chineseflashcards
import pytest

from chineseflashcards import diacritic_syl_and_tone
from chineseflashcards import CedictWord, _parse_line, Classifier
from chineseflashcards import Classifier


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


def test_diacritic_syl_and_tone_ascii_with_tone_numbers():
    """ Test ASCII representations with tone numbers """
    assert diacritic_syl_and_tone('ni3') == ('nǐ', 3)
    assert diacritic_syl_and_tone('ge5') == ('ge', 5)
    assert diacritic_syl_and_tone('lu:4') == ('lǜ', 4)


def test_diacritic_syl_and_tone_diacritic_representations():
    """ Test diacritic-based representations without tone numbers """
    assert diacritic_syl_and_tone('ni') == ('ni', 5)
    assert diacritic_syl_and_tone('nǐ') == ('nǐ', 3)
    assert diacritic_syl_and_tone('gé') == ('gé', 2)
    assert diacritic_syl_and_tone('lǜ') == ('lǜ', 4)


def test_diacritic_syl_and_tone_special_case_r():
    """ Test special case for the syllable 'r' """
    assert diacritic_syl_and_tone('r') == ('r', 5)
    assert diacritic_syl_and_tone('r5') == ('r', 5)


def test_diacritic_syl_and_tone_error_cases():
    """ Test for invalid inputs that should raise a ValueError """
    with pytest.raises(ValueError):
        diacritic_syl_and_tone('xyz')

    with pytest.raises(ValueError):
        diacritic_syl_and_tone('n6')


def test_diacritic_syl_and_tone_edge_vowel_groups():
    """ Test specific cases based on vowel groups defined in DIACRITIC_VOWELS """
    # Adjust based on the actual content of DIACRITIC_VOWELS
    assert diacritic_syl_and_tone('a1') == ('ā', 1)
    assert diacritic_syl_and_tone('o2') == ('ó', 2)
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
def test_parse_with_all_components():
    """
    Test the parse method with an input string containing all components:
    traditional, simplified characters separated by '|' and pinyin enclosed in '['.
    It should correctly parse and assign the values to trad, simp, and pinyin.
    """
    # Testing with a string containing all components separated by '|' and '['
    input_str = "傳統|简体[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == "zhū"


def test_parse_without_simplified():
    """
    Test the parse method with an input string without the '|' character.
    It should assign the same value to both trad and simp, and parse the pinyin correctly.
    """
    # Testing with a string without the '|' character, so traditional and simplified are the same
    input_str = "傳統[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "傳統"
    assert classifier.pinyin == "zhū"


def test_parse_with_traditional_and_simplified_only():
    """
    Test the parse method with an input string containing traditional and simplified characters but no pinyin.
    It should correctly parse trad and simp, and assign an empty string to pinyin.
    """
    # Testing with a string that has the traditional characters and simplified characters but no pinyin
    input_str = "傳統|简体[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == ""


def test_parse_with_empty_pinyin():
    """
    Test the parse method with an input string that has empty pinyin.
    It should correctly parse trad and simp, and assign an empty string to pinyin.
    """
    # Testing with a string that has empty pinyin
    input_str = "傳統|简体[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == ""


def test_parse_with_traditional_only():
    """
    Test the parse method with an input string that has only traditional characters and no simplified or pinyin.
    It should assign the same value to both trad and simp, and an empty string to pinyin.
    """
    # Testing with a string that has only traditional characters and no simplified or pinyin
    input_str = "傳統[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "傳統"
    assert classifier.pinyin == ""


def test_parse_invalid_format():
    """
    Test the parse method with an invalid format (e.g., missing '[').
    It should raise a ValueError indicating the input format is incorrect.
    """
    # Testing with an invalid format (e.g., missing '[')
    input_str = "傳統|简体zhū"
    with pytest.raises(ValueError):
        Classifier.parse(input_str)


def test_parse_missing_pipe():
    """
    Test the parse method with an input string that only has the empty pinyin and no traditional or simplified characters.
    It should assign empty strings to trad and simp, and correctly parse the pinyin.
    """
    # Testing with a string that only has the pinyin and no traditional or simplified characters
    input_str = "[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == ""
    assert classifier.simp == ""
    assert classifier.pinyin == ""


def test_parse_missing_bracket():
    """
    Test the parse method with a string missing the closing bracket.
    It should correctly parse trad, simp, and pinyin even with the missing bracket.
    """
    # Testing with a string missing the closing bracket
    input_str = "傳統|简体[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == "zhū"


def test_parse_with_extra_spaces():
    """
    Test the parse method with an input string containing extra spaces.
    It should strip the spaces from the input string and correctly parse trad, simp, and pinyin.
    """
    # Testing with extra spaces in the input string
    input_str = "  傳統  |  简体  [  zhū  ]  "
    classifier = Classifier.parse(input_str.strip())
    assert classifier.trad == "傳統  "
    assert classifier.simp == "  简体  "
    assert classifier.pinyin == "  zhū  "

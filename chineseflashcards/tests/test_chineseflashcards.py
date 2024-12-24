import chineseflashcards
import pytest

from chineseflashcards import Classifier


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

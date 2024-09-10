import chineseflashcards
import pytest

from chineseflashcards import Classifier


def test_diacritic_syl_r():
    assert chineseflashcards.diacritic_syl('r') == 'r'


def test_diacritic_syl_and_tone_r():
    assert chineseflashcards.diacritic_syl_and_tone('r') == ('r', 5)


def test_parse_with_all_components():
    # Testing with a string containing all components separated by '|' and '['
    input_str = "傳統|简体[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == "zhū"


def test_parse_without_simplified():
    # Testing with a string without the '|' character, so traditional and simplified are the same
    input_str = "傳統[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "傳統"
    assert classifier.pinyin == "zhū"


def test_parse_with_traditional_and_simplified_only():
    # Testing with a string that has the traditional characters and simplified characters but no pinyin
    input_str = "傳統|简体[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == ""


def test_parse_with_empty_pinyin():
    # Testing with a string that has empty pinyin
    input_str = "傳統|简体[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == ""


def test_parse_with_traditional_only():
    # Testing with a string that has only traditional characters and no simplified or pinyin
    input_str = "傳統[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "傳統"
    assert classifier.pinyin == ""


def test_parse_invalid_format():
    # Testing with an invalid format (e.g., missing '[')
    input_str = "傳統|简体zhū"
    with pytest.raises(ValueError):
        Classifier.parse(input_str)


def test_parse_missing_pipe():
    # Testing with a string that only has the pinyin and no traditional or simplified characters
    input_str = "[]"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == ""
    assert classifier.simp == ""
    assert classifier.pinyin == ""


def test_parse_missing_bracket():
    # Testing with a string missing the closing bracket
    input_str = "傳統|简体[zhū"
    classifier = Classifier.parse(input_str)
    assert classifier.trad == "傳統"
    assert classifier.simp == "简体"
    assert classifier.pinyin == "zhū"


def test_parse_with_extra_spaces():
    # Testing with extra spaces in the input string
    input_str = "  傳統  |  简体  [  zhū  ]  "
    classifier = Classifier.parse(input_str.strip())
    assert classifier.trad == "傳統  "
    assert classifier.simp == "  简体  "
    assert classifier.pinyin == "  zhū  "

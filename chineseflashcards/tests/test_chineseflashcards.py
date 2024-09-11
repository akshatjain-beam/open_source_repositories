import chineseflashcards
import pytest

from chineseflashcards import CedictWord, _parse_line, Classifier


def compare_cedict_words(word1, word2):
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
    assert chineseflashcards.diacritic_syl('r') == 'r'


def test_diacritic_syl_and_tone_r():
    assert chineseflashcards.diacritic_syl_and_tone('r') == ('r', 5)


def test_parse_line_basic():
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
    line = "Invalid line format"
    with pytest.raises(AttributeError):
        _parse_line(line)


def test_parse_line_multiple_categories():
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

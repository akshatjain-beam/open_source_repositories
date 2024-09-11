import chineseflashcards
import pytest

from chineseflashcards import diacritic_syl_and_tone


def test_diacritic_syl_r():
    assert chineseflashcards.diacritic_syl('r') == 'r'


def test_diacritic_syl_and_tone_r():
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

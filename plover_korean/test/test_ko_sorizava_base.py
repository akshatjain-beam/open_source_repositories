import pytest

from plover_korean.system.sorizava.dictionaries.ko_sorizava_base import INITIAL

def test_positive_cases():
    """
    Test the positive cases for the INITIAL dictionary.
    
    This function tests the positive cases where each Hangul consonant (key) is correctly mapped to its
    decomposed form (value) as defined in the INITIAL dictionary.
    """
    assert INITIAL['ㄱ'] == 'ㄱ'
    assert INITIAL['ㄲ'] == 'ㄱㅎ'
    assert INITIAL['ㄴ'] == 'ㄴ'
    assert INITIAL['ㄷ'] == 'ㄷ'
    assert INITIAL['ㄸ'] == 'ㄷㄹ'
    assert INITIAL['ㄹ'] == 'ㄹ'
    assert INITIAL['ㅁ'] == 'ㅁ'
    assert INITIAL['ㅂ'] == 'ㅂ'
    assert INITIAL['ㅃ'] == 'ㅂㄱ'
    assert INITIAL['ㅅ'] == 'ㅅ'
    assert INITIAL['ㅆ'] == 'ㅅㅁ'
    assert INITIAL['ㅇ'] == ''
    assert INITIAL['ㅈ'] == 'ㅈ'
    assert INITIAL['ㅉ'] == 'ㅈㄴ'
    assert INITIAL['ㅊ'] == 'ㅊ'
    assert INITIAL['ㅋ'] == 'ㅋ'
    assert INITIAL['ㅌ'] == 'ㅌ'
    assert INITIAL['ㅍ'] == 'ㅍ'
    assert INITIAL['ㅎ'] == 'ㅎ'

def test_negative_cases():
    """
    Test the negative cases for the INITIAL dictionary.
    
    This function tests negative cases where the keys are not present in the INITIAL dictionary.
    It asserts that accessing these keys should raise a KeyError.
    """
    with pytest.raises(KeyError):
        _ = INITIAL['ㅉㄴ']
    with pytest.raises(KeyError):
        _ = INITIAL['ㅋㅋ']
    with pytest.raises(KeyError):
        _ = INITIAL['ㄻ']
    with pytest.raises(KeyError):
        _ = INITIAL['ㅥ']
    with pytest.raises(KeyError):
        _ = INITIAL['ㅩ']

def test_edge_cases():
    """
    Test the edge cases for the INITIAL dictionary.
    
    This function tests edge cases such as empty input, single character that is not a valid key,
    and checks if accessing non-string types raises appropriate errors.
    """
    with pytest.raises(KeyError):
        _ = INITIAL['']  # Empty input
    
    with pytest.raises(KeyError):
        _ = INITIAL['a']  # Non-Hangul character
    
    with pytest.raises(KeyError):
        _ = INITIAL[None]  # None as input
    
    with pytest.raises(KeyError):
        _ = INITIAL[1]  # Integer as input

def test_positive_case_additional():
    """
    Test additional positive cases for the INITIAL dictionary.
    
    This function tests an additional positive case for a consonant with known decomposition.
    """
    assert INITIAL['ㄴ'] == 'ㄴ'  # Valid initial consonant with no decomposition needed

def test_negative_case_additional():
    """
    Test additional negative cases for the INITIAL dictionary.
    
    This function tests an additional negative case with a string that is not a valid initial consonant.
    """
    with pytest.raises(KeyError):
        _ = INITIAL['invalid']


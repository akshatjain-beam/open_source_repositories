import pytest

from src.abnf1.grammars import rfc4647
from src.abnf1.parser import ParseError

@pytest.mark.parametrize('src', [
# test added thanks to https://github.com/declaresub/abnf/issues/10.
'en',
'en-US',
])
def test_language_range(src: str):
    ip6 = rfc4647.Rule('language-range')
    assert ip6.parse_all(src)


@pytest.mark.parametrize('src', [
# test added thanks to https://github.com/declaresub/abnf/issues/10.
'*-*-foo',
])
def test_extended_language_range(src: str):
    ip6 = rfc4647.Rule('extended-language-range')
    assert ip6.parse_all(src)

#------------------

@pytest.mark.parametrize('src', [
'* *',
])
def test_extended_language_range(src: str):
    """Test parsing of an invalid extended-language-range with spaces.
    
    The input '* *' is not a valid representation according to the grammar rules
    because it contains spaces that are not allowed in a valid extended-language-range.
    The expectation is that this input will raise a ParseError.
    """
    ip6 = rfc4647.Rule('extended-language-range')
    with pytest.raises(ParseError):
        assert ip6.parse_all(src)


@pytest.mark.parametrize('src', [
'*-en',
])
def test_extended_language_range(src: str):
    """Test parsing of a valid extended-language-range with a wildcard prefix.
    
    The input '*-en' is a valid representation where:
    - '*' represents a wildcard that can match any language.
    - '-en' indicates the specific subtag for English.
    
    The expectation is that this input should be successfully parsed without raising an error.
    """
    ip6 = rfc4647.Rule('extended-language-range')
    assert ip6.parse_all(src)

@pytest.mark.parametrize('src', [
    'es-MX',  
])
def test_extended_language_range_valid_country_code(src: str):
    """Test parsing of a valid extended-language-range with a country code.
    
    The input 'es-MX' is a valid representation where:
    - 'es' represents the language (Spanish).
    - 'MX' represents the region (Mexico).
    
    The expectation is that the input should be successfully parsed without raising an error.
    """
    ip6 = rfc4647.Rule('extended-language-range')
    assert ip6.parse_all(src)

@pytest.mark.parametrize('src', [
    'fr-*',  
])
def test_extended_language_range_valid_with_wildcard(src: str):
    """Test parsing of a valid extended-language-range with a wildcard.
    
    The input 'fr-*' indicates that any subtag can follow the French language.
    The expectation is that the input should be successfully parsed without raising an error.
    """
    ip6 = rfc4647.Rule('extended-language-range')
    assert ip6.parse_all(src)

@pytest.mark.parametrize('src', [
    'en--US',  
])
def test_extended_language_range_invalid_double_hyphen(src: str):
    """Test parsing of an invalid extended-language-range due to double hyphen.
    
    The input 'en--US' is not a valid representation because it contains a double hyphen,
    which is not allowed in the specified grammar rules. 
    
    The expectation is that this input will raise a ParseError.
    """
    ip6 = rfc4647.Rule('extended-language-range')
    with pytest.raises(ParseError):
        assert ip6.parse_all(src)

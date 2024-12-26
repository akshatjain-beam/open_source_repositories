from src.abnf1.grammars.rfc2616 import Rule


def test_token():
    # exercise rule imported by hand from RFC 2616.
    src = "token"
    assert Rule("token").parse_all(src)



def test_token_valid_exclamation():
    """Test the token rule with a single valid character: '!' 
    This test verifies that the character '!' is correctly recognized as a valid token 
    according to the ABNF grammar rules defined in RFC 2616.

    Expected Outcome:
        - The parsing should succeed, and the result should not be None.
    """
    src = "!"
    assert Rule("token").parse_all(src)


def test_token_valid_hash():
    """Test the token rule with a single valid character: '#'
    This test ensures that the character '#' is identified as a valid token 
    according to the token rule in the ABNF grammar.

    Expected Outcome:
        - The parsing should succeed, indicating that '#' is a valid token.
    """
    src = "#"
    assert Rule("token").parse_all(src)


def test_token_valid_alphanumeric():
    """Test the token rule with an alphanumeric string: 'abc123'
    This test checks that a combination of letters and numbers is recognized 
    as a valid token according to the ABNF grammar rules.

    Expected Outcome:
        - The parsing should succeed, confirming that 'abc123' is a valid token.
    """
    src = "abc123"
    assert Rule("token").parse_all(src)


def test_token_valid_special_characters():
    """Test the token rule with a string containing special characters: '+-*.'
    This test verifies that a valid token made up of special characters is parsed 
    correctly according to the defined grammar rules.

    Expected Outcome:
        - The parsing should succeed, indicating that the combination '+-*.' is a valid token.
    """
    src = "+-*."
    assert Rule("token").parse_all(src)


def test_token_valid_combination():
    """Test the token rule with a mixed alphanumeric string: 'A1B2C3'
    This test checks that a string with both uppercase letters and numbers is 
    recognized as a valid token according to the ABNF grammar rules.

    Expected Outcome:
        - The parsing should succeed, confirming that 'A1B2C3' is a valid token.
    """
    src = "A1B2C3"
    assert Rule("token").parse_all(src)

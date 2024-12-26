"""
Collected rules from RFC 4647
https://tools.ietf.org/html/rfc4647
"""

from src.abnf1.parser import Rule as _Rule
from .misc import load_grammar_rules


@load_grammar_rules()
class Rule(_Rule):
    """Rule objects generated from ABNF in RFC 4647."""

    grammar = [
        'language-range = (1*8ALPHA *("-" 1*8alphanum)) / "*"',
        "alphanum = ALPHA / DIGIT",
        """
        Define an `extended-language-range` using ABNF (Augmented Backus-Naur Form) syntax.

        The `extended-language-range` consists of:
        - One or more (`1*`) sequences of 8-bit alphabetic characters (ALPHA) or a single asterisk ("*").
        - Optionally followed by zero or more repetitions (`*`) of a hyphen ("-") followed by one or more (`1*`) 
        alphanumeric characters (alphanum) or another asterisk ("*").
        """
        $PlaceHolder$
    ]

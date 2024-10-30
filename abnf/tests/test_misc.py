import typing

import pytest

from src.abnf1.grammars.misc import load_grammar, load_grammar_rules
from src.abnf1.parser import Literal
from src.abnf1.parser import Rule as _Rule


class ImportRule(_Rule):
    pass


ImportRule("test", Literal("test"))


@load_grammar_rules([("test", ImportRule("test"))])
class Rule(_Rule):
    grammar: typing.List[str] = []


def test_misc_load_grammar_rules_import():
    assert Rule("test").definition == ImportRule("test").definition


@load_grammar([("test", ImportRule("test"))])
class Rule1(_Rule):
    grammar: str = ''

def test_load_grammar():
    assert Rule("test").definition == ImportRule("test").definition


class Foo(_Rule):
    grammar = 'foo="bar"'


def test_load_grammar_rules_str():
    with pytest.raises(TypeError):
        load_grammar_rules()(Foo)


class Bar(_Rule):
    grammar = ['foo="bar"']


def test_load_grammar_list():
    with pytest.raises(TypeError):
        load_grammar()(Bar)

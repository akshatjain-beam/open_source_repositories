# import pytest
# import src.abnf1.grammars
# import pkgutil
# from importlib import import_module
# import types

# @pytest.mark.parametrize("rfc", map(import_module, ['%s.%s' % (src.abnf1.grammars.__name__, x[1]) for x in pkgutil.walk_packages(src.abnf1.grammars.__path__) if x[1] == 'cors' or x[1].startswith('rfc')]))
# def test_grammar(rfc: types.ModuleType):
#     """Catches rules used but not defined in grammar."""
#     for rule in rfc.Rule.rules():
#         if not hasattr(rule, 'definition'):
#             print(str(rule))
#         assert hasattr(rule, 'definition')

# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.cbv` module.
"""

from bottle_neck.cbv import BaseHandlerPlugin


class TestBaseHandlerPlugin:
    def setup_method(self):
        self.plugin = BaseHandlerPlugin(lambda x: x, 1, 2, a=3, b=4)
        self.clear_cache()

    def clear_cache(self):
        """Clears the cached properties to ensure tests start with a fresh state."""
        try:
            del self.plugin.__class__.__cache  # Reset the cache
        except AttributeError:
            pass  # If there's no cache, we can safely ignore this

    def test_func_name_with_camel_case(self):
        """
        Test that func_name correctly converts camel case to snake case
        """
        class CamelCasePlugin(BaseHandlerPlugin):
            pass
        plugin = CamelCasePlugin(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == 'camel_case_plugin'  # This should be the expected result

    def test_func_name_with_multiple_camel_case(self):
        """
        Test that func_name correctly converts multiple camel case to snake case
        """
        class MultipleCamelCasePlugin(BaseHandlerPlugin):
            pass
        plugin = MultipleCamelCasePlugin(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == 'multiple_camel_case_plugin'  # This should be the expected result

    def test_func_name_with_underscore(self):
        """
        Test that func_name correctly handles class name with underscore
        """
        class Plugin_With_Underscore(BaseHandlerPlugin):
            pass
        plugin = Plugin_With_Underscore(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == 'plugin__with__underscore'

    def test_func_name_with_numbers_in_class_name(self):
        """
        Test that func_name correctly handles class name with numbers
        """
        class Plugin123(BaseHandlerPlugin):
            pass
        plugin = Plugin123(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == 'plugin123'
    
    def test_func_name_with_numbers_and_words_in_class_name(self):
        """
        Test that func_name correctly handles class name with numbers and camel case
        """
        class Plugin123Case(BaseHandlerPlugin):
            pass
        plugin = Plugin123Case(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == 'plugin123_case'  # Expected result after conversion

    def test_func_name_with_empty_class_name(self):
        """
        Test that func_name correctly handles empty class name
        """
        class _(BaseHandlerPlugin):
            pass
        plugin = _(lambda x: x, 1, 2, a=3, b=4)
        assert plugin.func_name == '_'

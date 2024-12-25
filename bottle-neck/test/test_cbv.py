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

import inspect
from bottle_neck.cbv import BaseHandler


class TestBuildRoutes:
    def test_no_args(self):
        """
        Test the behavior when no method arguments are provided.

        This test checks that when `method_args` is an empty dictionary and no
        `url_extra_part` is given, the method returns a list containing only
        the base endpoint, which should be '/'.
        """

        method_args = {}
        url_extra_part = None
        expected = ['/']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_single_arg(self):
        """
        Test the behavior with a single argument.

        This test verifies that when `method_args` contains one argument,
        the method returns a list with the base endpoint and an endpoint
        that includes the single argument as a dynamic parameter (/:arg1).
        """

        method_args = {'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None)}
        url_extra_part = None
        expected = ['/', '/:arg1']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_multiple_args(self):
        """
        Test the behavior with multiple arguments.

        This test checks that when `method_args` contains two arguments,
        the method returns a list with the base endpoint and two endpoints,
        each including one of the arguments as dynamic parameters (/:arg1 and /:arg2).
        """

        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None)
        }
        url_extra_part = None
        expected = ['/', '/:arg1', '/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_arg_with_default(self):
        """
        Test the behavior with an argument that has a default value.

        This test verifies that when `method_args` contains an argument
        with a default value, the method returns a single endpoint
        that includes the argument as a dynamic parameter (/:arg1).
        """

        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value')
        }
        url_extra_part = None
        expected = ['/:arg1']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_multiple_args_with_defaults(self):
        """
        Test the behavior with multiple arguments that have default values.

        This test checks that when `method_args` contains two arguments,
        both with default values, the method returns a single endpoint
        that includes both arguments as dynamic parameters (/:arg1/:arg2).
        """

        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value1'),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value2')
        }
        url_extra_part = None
        expected = ['/:arg1/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_mixed_args(self):
        """
        Test the behavior with a mix of arguments with and without default values.

        This test verifies that when `method_args` contains a mix of
        arguments, some with default values and some without, the method
        returns endpoints for all combinations of these arguments as dynamic
        parameters. Specifically, it checks for two different combinations:
        1. /:arg1/:arg3
        2. /:arg1/:arg3/:arg2
        """

        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value'),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None),
            'arg3': inspect.Parameter('arg3', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value')
        }
        url_extra_part = None
        expected = ['/:arg1/:arg3', '/:arg1/:arg3/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected
import pytest
from bottle_neck.cbv import classproperty, cached_classproperty


class ExampleClass:
    _value = 0

    @classproperty
    def value(cls):
        return cls._value

    @classproperty
    def value_with_set(cls):
        return cls._value


class TestExampleClass:

    def test_class_property_get(self):
        assert ExampleClass.value == 0  # Test initial value

    def test_class_property_set(self):
        ExampleClass._value = 42
        assert ExampleClass.value == 42  # Verify getter reflects the new value

    def test_class_property_get_after_set(self):
        ExampleClass._value = 100  # Set the class attribute
        assert ExampleClass.value == 100  # Verify getter reflects the updated value

    def test_class_property_set_large_value(self):
        ExampleClass._value = 1_000_000
        assert ExampleClass.value == 1_000_000  # Verify getter reflects large value

    def test_class_property_set_negative_value(self):
        ExampleClass._value = -50
        assert ExampleClass.value == -50  # Verify getter reflects negative value

    def test_class_property_get_on_modified_class(self):
        class AnotherClass(ExampleClass):
            _value = 200

        assert AnotherClass.value == 200  # Check that subclass inherits modified value

    def test_class_property_get_empty_class(self):
        class EmptyClass:
            @classproperty
            def empty_value(cls):
                return None

        assert EmptyClass.empty_value is None  # Test that property returns None

    def test_class_property_edge_case_zero(self):
        ExampleClass._value = 0
        assert ExampleClass.value == 0  # Edge case with zero


class TestClass:
    @cached_classproperty
    def value(cls):
        return 42

    @cached_classproperty
    def another_value(cls):
        return 24

    @cached_classproperty
    def exception_value(cls):
        raise ValueError("Test exception")

    @cached_classproperty
    def none_value(cls):
        return None


@pytest.fixture(autouse=True)
def clear_cache():
    # Clear the cache before each test
    TestClass.__cache = {}


def test_cached_classproperty():
    """
    Test that the cached_classproperty decorator caches the value correctly.

    This test checks if the value property is computed and cached correctly.
    It also verifies that the cache contains the computed value.
    """
    assert TestClass.value == 42
    assert hasattr(TestClass, '__cache')

    value_func = next(
        key for key in TestClass.__cache if key.__name__ == 'value')
    assert TestClass.__cache[value_func] == 42


def test_cached_classproperty_multiple_access():
    """
    Test that the value is cached and not recomputed on multiple accesses.

    This test ensures that accessing the cached property multiple times does
    not recompute the value and uses the cached value instead.
    """
    assert TestClass.value == 42
    assert TestClass.value == 42
    assert len(TestClass.__cache) == 1


def test_cached_classproperty_multiple_properties():
    """
    Test that multiple properties are cached correctly.

    This test checks if multiple cached properties are stored correctly
    in the cache without interfering with each other.
    """
    assert TestClass.value == 42
    assert TestClass.another_value == 24
    assert len(TestClass.__cache) == 2


def test_cached_classproperty_exception():
    """
    Test that an exception is raised when accessing a property that raises an exception.

    This test verifies that accessing a cached property which raises an exception
    correctly raises the intended exception.
    """
    with pytest.raises(ValueError):
        TestClass.exception_value


def test_cached_classproperty_none():
    """
    Test that a property that returns None is cached correctly.

    This test checks if a property returning None is properly cached
    and stored in the cache.
    """
    assert TestClass.none_value is None
    assert len(TestClass.__cache) == 1


def test_cached_classproperty_reset_cache():
    """
    Test that the cache is reset when the class is redefined.

    This test ensures that redefining a class resets the cache,
    ensuring no old cached values are present.
    """
    class NewTestClass:
        @cached_classproperty
        def value(cls):
            return 42

    assert NewTestClass.value == 42
    assert len(NewTestClass.__cache) == 1


def test_cached_classproperty_inheritance():
    """
    Test that the cache is inherited by subclasses.

    This test checks if subclasses inherit the cache from their parent class
    and use it correctly.
    """
    class SubClass(TestClass):
        pass

    assert SubClass.value == 42
    assert len(SubClass.__cache) == 1


def test_cached_classproperty_override():
    """
    Test that a subclass can override a cached property.

    This test verifies that subclasses can override a cached property
    and the new value is cached correctly without affecting the parent class cache.
    """
    class SubClass(TestClass):
        @cached_classproperty
        def value(cls):
            return 24

    assert SubClass.value == 24
    assert len(SubClass.__cache) == 1
    assert TestClass.value == 42

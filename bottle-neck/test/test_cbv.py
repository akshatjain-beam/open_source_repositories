# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.cbv` module.
"""

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
    assert TestClass.value == 42
    assert hasattr(TestClass, '__cache')

    value_func = next(
        key for key in TestClass.__cache if key.__name__ == 'value')
    assert TestClass.__cache[value_func] == 42


def test_cached_classproperty_multiple_access():
    # Test that the value is cached and not recomputed on multiple access
    assert TestClass.value == 42
    assert TestClass.value == 42
    assert len(TestClass.__cache) == 1


def test_cached_classproperty_multiple_properties():
    # Test that multiple properties are cached correctly
    assert TestClass.value == 42
    assert TestClass.another_value == 24
    assert len(TestClass.__cache) == 2


def test_cached_classproperty_exception():
    # Test that an exception is raised when accessing a property that raises an exception
    with pytest.raises(ValueError):
        TestClass.exception_value


def test_cached_classproperty_none():
    # Test that a property that returns None is cached correctly
    assert TestClass.none_value is None
    assert len(TestClass.__cache) == 1


def test_cached_classproperty_reset_cache():
    # Test that the cache is reset when the class is redefined
    class NewTestClass:
        @cached_classproperty
        def value(cls):
            return 42

    assert NewTestClass.value == 42
    assert len(NewTestClass.__cache) == 1


def test_cached_classproperty_inheritance():
    # Test that the cache is inherited by subclasses
    class SubClass(TestClass):
        pass

    assert SubClass.value == 42
    assert len(SubClass.__cache) == 1


def test_cached_classproperty_override():
    # Test that a subclass can override a cached property
    class SubClass(TestClass):
        @cached_classproperty
        def value(cls):
            return 24

    assert SubClass.value == 24
    assert len(SubClass.__cache) == 1
    assert TestClass.value == 42

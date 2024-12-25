#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2020 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     Santiago Dueñas <sduenas@bitergia.com>
#     Miguel Ángel Fernández <mafesan@bitergia.com>
#     Valerio Cosentino <valcos@bitergia.com>
#     Jesus M. Gonzalez-Barahona <jgb@gsyc.es>
#

import unittest

from grimoirelab_toolkit.introspect import (inspect_signature_parameters,
                                            find_signature_parameters,
                                            find_class_properties)


class FakeCallable:
    """Fake class for testing introspection."""

    def __init__(self, *args, **kwargs):
        pass

    def test_args(self, a, **kwargs):
        pass

    def test(self, a, b, c=None):
        pass

    @classmethod
    def class_test(cls, a, b):
        pass

    @staticmethod
    def static_test(a, b):
        pass


class TestInspectSignatureParameters(unittest.TestCase):
    """Unit tests for inspect_signature_parameters."""

    def test_inspect(self):
        """
        Test retrieving parameters from various callables.

        This test checks the parameters of different methods and functions
        in the FakeCallable class, ensuring that the expected parameters 
        match the actual parameters retrieved. Each method's parameters 
        are asserted against predefined expected lists.

        Expectations:
        - FakeCallable should return ['args', 'kwargs']
        - __init__ should return ['self', 'args', 'kwargs']
        - test should return ['self', 'a', 'b', 'c']
        - class_test should return ['a', 'b']
        - static_test should return ['a', 'b']
        """

        expected = ['args', 'kwargs']
        params = inspect_signature_parameters(FakeCallable)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['self', 'args', 'kwargs']
        params = inspect_signature_parameters(FakeCallable.__init__)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['self', 'a', 'b', 'c']
        params = inspect_signature_parameters(FakeCallable.test)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['a', 'b']
        params = inspect_signature_parameters(FakeCallable.class_test)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['a', 'b']
        params = inspect_signature_parameters(FakeCallable.static_test)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

    def test_inspect_excluding_parameters(self):
        """
        Test retrieving parameters while excluding certain ones.

        This test checks the parameters of various methods and functions in 
        FakeCallable while excluding specific parameters ('self', 'cls', and 'a'). 
        It verifies that the excluded parameters do not appear in the output.

        Expectations:
        - FakeCallable should return ['args', 'kwargs']
        - test should return ['b', 'c']
        - class_test should return ['b']
        - static_test should return ['b']
        """

        excluded = ['self', 'cls', 'a']

        expected = ['args', 'kwargs']
        params = inspect_signature_parameters(FakeCallable,
                                              excluded=excluded)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['b', 'c']
        params = inspect_signature_parameters(FakeCallable.test,
                                              excluded=excluded)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['b']
        params = inspect_signature_parameters(FakeCallable.class_test,
                                              excluded=excluded)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

        expected = ['b']
        params = inspect_signature_parameters(FakeCallable.static_test,
                                              excluded=excluded)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

    def test_inspect_no_parameters(self):
        """
        Test a callable with no parameters.

        This test verifies that a function defined with no parameters returns
        an empty list. It ensures that the inspect_signature_parameters function
        can handle callables without any parameters gracefully.

        Expectation:
        - A callable with no parameters should return an empty list.
        """

        def no_params():
            pass

        expected = []
        params = inspect_signature_parameters(no_params)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

    def test_inspect_keyword_only_parameters(self):
        """
        Test a callable with keyword-only parameters.

        This test checks a function that defines parameters as keyword-only.
        It verifies that the parameters are correctly returned and not confused
        with positional parameters.

        Expectation:
        - A function with keyword-only parameters should return ['a', 'b'].
        """

        def keyword_only(*, a, b=2):
            pass

        expected = ['a', 'b']
        params = inspect_signature_parameters(keyword_only)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)
    
    def test_inspect_mixed_parameters(self):
        """
        Test a callable with mixed types of parameters.

        This test checks a function that has a mix of positional-only, positional,
        and keyword-only parameters. It verifies that all parameters are 
        correctly returned.

        Expectation:
        - A function with mixed parameters should return ['a', 'b', 'c'].
        """

        def mixed_params(a, /, b, *, c):
            pass

        expected = ['a', 'b', 'c']
        params = inspect_signature_parameters(mixed_params)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)

    def test_inspect_excluding_defaults(self):
        """
        Test a callable with parameters that have default values.

        This test verifies that when parameters with default values are excluded,
        the remaining parameters are correctly returned. It ensures that the 
        function can exclude parameters regardless of their default status.

        Expectation:
        - A function with parameters 'a', 'b=2', and 'c=3' should return ['a'] 
        when 'b' and 'c' are excluded.
        """

        def defaults(a, b=2, c=3):
            pass

        excluded = ['b', 'c']

        expected = ['a']
        params = inspect_signature_parameters(defaults, excluded=excluded)
        params = [p.name for p in params]
        self.assertListEqual(params, expected)


class TestFindSignatureParameters(unittest.TestCase):
    """Unit tests for find_signature_parameters."""

    def test_find_parameters(self):
        """Test if a list of parameters is generated."""

        expected = {'a': 1, 'b': 2, 'c': 3}
        params = {'a': 1, 'b': 2, 'c': 3}
        found = find_signature_parameters(FakeCallable.test, params)
        self.assertDictEqual(found, expected)

        expected = {'a': 1, 'b': 2, 'c': 3}
        params = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        found = find_signature_parameters(FakeCallable.test, params)
        self.assertDictEqual(found, expected)

        expected = {'a': 1, 'b': 2}
        params = {'a': 1, 'b': 2, 'd': 3}
        found = find_signature_parameters(FakeCallable.test, params)
        self.assertDictEqual(found, expected)

        expected = {'a': 1, 'b': 2}
        params = {'a': 1, 'b': 2}
        found = find_signature_parameters(FakeCallable.test_args, params)
        self.assertDictEqual(found, expected)

    def test_find_excluding_parameters(self):
        """Test if a list of parameters is generated excluding some."""

        expected = {'b': 2, 'c': 3}
        params = {'a': 1, 'b': 2, 'c': 3}
        excluded = ('self', 'a')
        found = find_signature_parameters(FakeCallable.test, params,
                                          excluded=excluded)
        self.assertDictEqual(found, expected)

    def test_attribute_error(self):
        """Test if it raises an exception for not found parameters."""

        with self.assertRaises(AttributeError) as e:
            params = {'a': 1, 'd': 3}
            _ = find_signature_parameters(FakeCallable.test, params)

        self.assertEqual(e.exception.args[1], 'b')


class PropertiesClass:
    """Class for testing properties finding."""

    def __init__(self):
        self.member = "not a property"
        self._readonly_property = True
        self._my_property = None

    @property
    def my_property(self):
        return self._my_property

    @my_property.setter
    def my_property(self, value):
        self._my_property = value

    @property
    def readonly_property(self):
        return self._readonly_property


class NoPropertiesClass:
    """Class for testing properties finding."""

    def __init__(self):
        self.member = "not a property"
        self.readonly_property = True
        self.my_property = None


class TestFindObjectProperties(unittest.TestCase):
    """Unit tests for find_class_properties."""

    def test_find_class_properties(self):
        """Test if properties are found in a class"""

        properties = find_class_properties(PropertiesClass)
        self.assertEqual(len(properties), 2)

        p = properties[0]
        self.assertEqual(p[0], 'my_property')
        self.assertIsInstance(p[1], property)

        p = properties[1]
        self.assertEqual(p[0], 'readonly_property')
        self.assertIsInstance(p[1], property)

    def test_find_no_properties(self):
        """Test if nothing is found in an object with no properties"""

        properties = find_class_properties(NoPropertiesClass())
        self.assertEqual(len(properties), 0)


if __name__ == "__main__":
    unittest.main(warnings='ignore')

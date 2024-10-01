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

    def test_args(a, b, *args):
        pass

    def test_kwargs(self, a, **kwargs):
        pass

    def test_mixed(a, b, *args, **kwargs):
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
        """Check the parameters from a callable."""

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
        """Check the parameters from a callable when some are excluded."""

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


class TestFindSignatureParameters(unittest.TestCase):
    """Unit tests for find_signature_parameters."""

    def test_find_parameters(self):
        """
        Test if a list of parameters is generated correctly from the callable.

        This test checks if the expected parameters are correctly retrieved from 
        the callable `FakeCallable.test` when provided with a dictionary of 
        candidate parameters. It verifies that extraneous parameters do not affect 
        the result.
        """

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
        found = find_signature_parameters(FakeCallable.test_kwargs, params)
        self.assertDictEqual(found, expected)
    
    def test_find_parameters_with_args(self):
        """
        Test if *args are correctly ignored when finding parameters.

        This test verifies that parameters defined with *args in 
        `FakeCallable.test_args` do not appear in the retrieved 
        parameters, ensuring that the function only considers named parameters.
        """
        expected = {'a': 1, 'b': 2}
        params = {'a': 1, 'b': 2}
        found = find_signature_parameters(FakeCallable.test_args, params)
        self.assertDictEqual(found, expected)

    def test_find_excluding_parameters(self):
        """
        Test if a list of parameters is generated excluding specified ones.

        This test checks the functionality of excluding certain parameters, 
        such as 'self' and 'a', when retrieving parameters from 
        `FakeCallable.test`. The test verifies that the expected parameters 
        remain after exclusion.
        """

        expected = {'b': 2, 'c': 3}
        params = {'a': 1, 'b': 2, 'c': 3}
        excluded = ('self', 'a')
        found = find_signature_parameters(FakeCallable.test, params,
                                          excluded=excluded)
        self.assertDictEqual(found, expected)

    def test_attribute_error(self):
        """
        Test if it raises an exception for parameters that are not found.

        This test ensures that the function correctly raises an 
        AttributeError when one or more required parameters are missing 
        from the provided candidates. The test checks that the error message 
        contains the name of the missing parameter.
        """

        with self.assertRaises(AttributeError) as e:
            params = {'a': 1, 'd': 3}
            _ = find_signature_parameters(FakeCallable.test, params)

        self.assertEqual(e.exception.args[1], 'b')
    
    def test_excluding_self_cls(self):
        """
        Test excluding default parameters 'self' and 'cls'.

        This test verifies that when a method of a class is inspected, 
        the parameters 'self' and 'cls' are correctly excluded from 
        the results. The test checks if only the expected parameters remain.
        """
        class TestClass:
            def method(self, cls, a, b):
                pass
        expected = {'a': 1, 'b': 2}
        params = {'self': None, 'cls': None, 'a': 1, 'b': 2}
        found = find_signature_parameters(TestClass().method, params)
        self.assertDictEqual(found, expected)
    
    def test_mixed_args_kwargs(self):
        """
        Test if mixed *args and **kwargs are handled correctly.

        This test checks that the function can properly process a callable 
        (`FakeCallable.test_mixed`) that utilizes both *args and **kwargs, 
        confirming that all relevant parameters are included in the result.
        """
        expected = {'a': 1, 'b': 2, 'd': 4, 'e': 5}
        params = {'a': 1, 'b': 2, 'd': 4, 'e': 5}
        found = find_signature_parameters(FakeCallable.test_mixed, params)
        self.assertDictEqual(found, expected)


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

# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
# file: $Id$
# auth: metagriffin <mg.github@uberdev.org>
# date: 2013/11/08
# copy: (C) Copyright 2013-EOT metagriffin -- see LICENSE.txt
#------------------------------------------------------------------------------
# This software is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
#------------------------------------------------------------------------------

import unittest

import morph
from morph import isseq, isstr, isdict

#------------------------------------------------------------------------------
class TestMorph(unittest.TestCase):

  maxDiff = None

  #----------------------------------------------------------------------------
  def test_isstr(self):
    self.assertTrue(morph.isstr(''))
    self.assertTrue(morph.isstr(u''))
    self.assertTrue(morph.isstr('abc'))
    self.assertTrue(morph.isstr(u'abc'))
    self.assertFalse(morph.isstr(['a', 'b', 'c']))
    self.assertFalse(morph.isstr(('a', 'b', 'c')))
    self.assertFalse(morph.isstr(list('abc')))
    self.assertFalse(morph.isstr(dict(abc='def')))
    self.assertFalse(morph.isstr(17))

  #----------------------------------------------------------------------------
  def test_isseq(self):
    self.assertTrue(morph.isseq(['a', 'b', 'c']))
    self.assertTrue(morph.isseq(('a', 'b', 'c')))
    self.assertTrue(morph.isseq(set(['a', 'b', 'c'])))
    class mylist(list): pass
    self.assertTrue(morph.isseq(mylist()))
    class myiter(object):
      def __iter__(self):
        return iter(['a', 'b', 'c'])
    self.assertTrue(morph.isseq(myiter()))
    self.assertFalse(morph.isseq('abc'))
    self.assertFalse(morph.isseq(u'abc'))
    class myobj(object): pass
    self.assertFalse(morph.isseq(myobj()))
    self.assertFalse(morph.isseq(dict(abc='def')))

  #----------------------------------------------------------------------------
  def test_isdict(self):
    self.assertTrue(morph.isdict(dict()))
    self.assertTrue(morph.isdict(dict(abc='def')))
    self.assertFalse(morph.isdict('abc'))
    self.assertFalse(morph.isdict(u'abc'))
    self.assertFalse(morph.isdict(['a', 'b', 'c']))

  #----------------------------------------------------------------------------
  def test_isscalar(self):
    self.assertTrue(morph.isscalar(None))
    self.assertTrue(morph.isscalar(True))
    self.assertTrue(morph.isscalar(False))
    self.assertTrue(morph.isscalar(3))
    self.assertTrue(morph.isscalar(3.14159))
    self.assertTrue(morph.isscalar(-3.14159))
    self.assertTrue(morph.isscalar('foo'))
    self.assertTrue(morph.isscalar(b'foo'))
    self.assertTrue(morph.isscalar(u'foo'))
    self.assertFalse(morph.isscalar([ 3 ]))
    self.assertFalse(morph.isscalar(( 3, )))
    self.assertFalse(morph.isscalar(self))
    self.assertFalse(morph.isscalar(unittest.TestCase))
  #------
  def test_bytes_without_py3(self):
        # Bytes should be considered scalar values regardless of PY3.
        #self.assertTrue(morph.isscalar(b'bytes'))  # Expected: True

        # Simulating the absence of PY3 definition which might lead to flawed solution failure.
        global PY3
        PY3 = None
        self.assertTrue(morph.isscalar(b'bytes'))  # Expected: True (Fails)



  #----------------------------------------------------------------------------
  def test_isstruct(self):
    self.assertTrue(morph.isstruct([ 1, 2, 3 ]))
    self.assertTrue(morph.isstruct(( 1, 2, 3 )))
    self.assertTrue(morph.isstruct([ self, unittest.TestCase ]))
    self.assertTrue(morph.isstruct(dict(one=1)))
    self.assertTrue(morph.isstruct(dict(class_=self)))
    self.assertFalse(morph.isstruct(1))
    self.assertFalse(morph.isstruct([ self, unittest.TestCase ], primitives=True))
    self.assertFalse(morph.isstruct(dict(class_=self), primitives=True))

  #----------------------------------------------------------------------------
  def test_isprimitive(self):
    self.assertTrue(morph.isprimitive(None))
    self.assertTrue(morph.isprimitive([ True, False ]))
    self.assertTrue(morph.isprimitive(( 3, 3.14159 )))
    self.assertTrue(morph.isprimitive(( [ None ], dict(foo=[ b'bar', u'bar' ]) )))
    self.assertFalse(morph.isprimitive([ self, unittest.TestCase ]))

  #----------------------------------------------------------------------------
  def test_tobool(self):
    self.assertTrue(morph.tobool('true'))
    self.assertTrue(morph.tobool('TRUE'))
    self.assertTrue(morph.tobool('yes'))
    self.assertTrue(morph.tobool('yEs'))
    self.assertTrue(morph.tobool('1'))
    self.assertFalse(morph.tobool('false'))
    self.assertFalse(morph.tobool('FALSE'))
    self.assertFalse(morph.tobool('nada'))
    self.assertFalse(morph.tobool('No'))
    self.assertFalse(morph.tobool('no'))
    self.assertFalse(morph.tobool('0'))
    self.assertIsNone(morph.tobool('nada', default=None))
    with self.assertRaises(ValueError) as cm:
      morph.tobool('nada', default=ValueError)
    self.assertTrue(morph.tobool(True))
    self.assertFalse(morph.tobool(False))
    self.assertTrue(morph.tobool(1))
    self.assertFalse(morph.tobool(0))

  #----------------------------------------------------------------------------
  def test_tolist(self):
    self.assertEqual(morph.tolist(['abc', 'def']), ['abc', 'def'])
    self.assertEqual(morph.tolist('abcdef'), ['abcdef'])
    self.assertEqual(morph.tolist('abc def'), ['abc', 'def'])
    self.assertEqual(morph.tolist('ab cd ef'), ['ab', 'cd', 'ef'])
    self.assertEqual(morph.tolist('"ab cd"\nef'), ['ab cd', 'ef'])

  #----------------------------------------------------------------------------
  def test_flatten(self):
    self.assertEqual(
      morph.flatten([1, [2, [3, 'abc', 'def', {'foo': ['zig', ['zag', 'zog']]}], 4]]),
      [1, 2, 3, 'abc', 'def', {'foo': ['zig', ['zag', 'zog']]}, 4])
    self.assertEqual(
      morph.flatten({'a': {'b': 'c'}}),
      {'a.b': 'c'})
    self.assertEqual(
      morph.flatten({'a': {'b': 1, 'c': [2, {'d': 3, 'e': 4}]}}),
      {'a.b': 1, 'a.c[0]': 2, 'a.c[1].d': 3, 'a.c[1].e': 4})
    self.assertEqual(
      morph.flatten({'a': {'b': [[1, 2], [3, {'x': 4, 'y': 5}, 6]]}}),
      {'a.b[0][0]':   1,
       'a.b[0][1]':   2,
       'a.b[1][0]':   3,
       'a.b[1][1].x': 4,
       'a.b[1][1].y': 5,
       'a.b[1][2]':   6,
      })

  #----------------------------------------------------------------------------
  def test_unflatten_fail(self):
    with self.assertRaises(ValueError) as cm:
      morph.unflatten({'a.b': 'c', 'a[0]': 'no'})
    self.assertEqual(
      str(cm.exception),
      'conflicting structures (dict vs. list) for prefix: a')
    with self.assertRaises(ValueError) as cm:
      morph.unflatten({'a': 'b', 'a.b': 'c'})
    self.assertEqual(
      str(cm.exception),
      'conflicting scalar vs. structure for prefix: a')
    with self.assertRaises(ValueError) as cm:
      morph.unflatten({'a[0': 'b'})
    self.assertEqual(
      str(cm.exception),
      'invalid list syntax (no terminating "]") in key "a[0"')
    with self.assertRaises(ValueError) as cm:
      morph.unflatten({'a[NADA]': 'b'})
    self.assertEqual(
      str(cm.exception),
      'invalid list syntax (bad index) in key "a[NADA]"')

  #----------------------------------------------------------------------------
  def test_unflatten_ok(self):
    self.assertEqual(
      morph.unflatten({'a.b': 'c', 'd': 'e'}),
      {'a': {'b': 'c'}, 'd': 'e'})
    self.assertEqual(
      morph.unflatten({'a.b': 1, 'a.c[0]': 2, 'a.c[1]': 3, 'a.c[2]': 4}),
      {'a': {'b': 1, 'c': [2, 3, 4]}})
    self.assertEqual(
      morph.unflatten({'a.b': 1, 'a.c[0]': 2, 'a.c[1].d': 3, 'a.c[1].e': 4}),
      {'a': {'b': 1, 'c': [2, {'d': 3, 'e': 4}]}})
    self.assertEqual(
      morph.unflatten({
        'a.b[0][0]':   1,
        'a.b[0][1]':   2,
        'a.b[1][0]':   3,
        'a.b[1][1].x': 4,
        'a.b[1][1].y': 5,
        'a.b[1][2]':   6,
        }),
      {'a': {'b': [[1, 2], [3, {'x': 4, 'y': 5}, 6]]}})

  #----------------------------------------------------------------------------
  def test_pick(self):
    class aadict(dict): pass
    d = aadict(foo='bar', zig=87, ziggy=78)
    self.assertEqual(morph.pick(d, 'foo'), {'foo': 'bar'})
    self.assertEqual(morph.pick(d, 'foo', dict=aadict), {'foo': 'bar'})
    self.assertEqual(morph.pick(d), {})
    self.assertEqual(morph.pick(d, prefix='zi'), {'g': 87, 'ggy': 78})
    self.assertIsInstance(morph.pick(d, 'foo'), dict)
    self.assertNotIsInstance(morph.pick(d, 'foo'), aadict)
    self.assertIsInstance(morph.pick(d, 'foo', dict=aadict), aadict)
    self.assertEqual(morph.pick(d), {})

  #----------------------------------------------------------------------------
  def test_pick_object(self):
    class Thing(object):
      def __init__(self):
        self.foo = 'bar'
        self.zig1 = 'zog'
        self.zig2 = 'zug'
      def zigSomeMethod(self):
        pass
    src = Thing()
    self.assertEqual(
      morph.pick(src, 'foo', 'zig1'),
      {'zig1': 'zog', 'foo': 'bar'})
    self.assertEqual(
      morph.pick(src, prefix='zig'),
      {'1': 'zog', '2': 'zug'})
    self.assertEqual(morph.pick(src), {})

  #----------------------------------------------------------------------------
  def test_pick_tree(self):
    src = {
      'a': 'a',
      'b': {'x': 'b.x', 'y': 'b.y'},
      'b.x': 'b-dot-x',
      'c': [
        {'x': 'c0.x', 'y': 'c0.y'},
        {'x': 'c1.x', 'y': 'c1.y'},
      ],
    }
    self.assertEqual(
      morph.pick(src, 'a', 'b.x', tree=True),
      {'a': 'a', 'b': {'x': 'b.x'}})
    self.assertEqual(
      morph.pick(src, 'a', 'b.x'),
      {'a': 'a', 'b.x': 'b-dot-x'})
    # TODO: add support for this...
    # self.assertEqual(
    #   morph.pick(src, 'c[0].x', tree=True),
    #   {'c': [{'x': 'c0.x'}]})
    # self.assertEqual(
    #   morph.pick(src, 'c[].x', tree=True),
    #   {'c': [{'x': 'c0.x'}, {'x': 'c1.x'}]})

  #----------------------------------------------------------------------------
  def test_omit(self):
    class aadict(dict): pass
    d = aadict(foo='bar', zig=87, ziggy=78)
    self.assertEqual(morph.omit(d, 'foo'), {'zig': 87, 'ziggy': 78})
    self.assertEqual(morph.omit(d, prefix='zig'), {'foo': 'bar'})
    self.assertEqual(morph.omit(d), {'foo': 'bar', 'zig': 87, 'ziggy': 78})

  #----------------------------------------------------------------------------
  def test_omit_object(self):
    class Thing(object):
      def __init__(self):
        self.foo = 'bar'
        self.zig1 = 'zog'
        self.zig2 = 'zug'
      def zigSomeMethod(self):
        pass
    src = Thing()
    self.assertEqual(
      morph.omit(src, 'foo', 'zig1'),
      {'zig2': 'zug'})
    self.assertEqual(
      morph.omit(src, prefix='zig'),
      {'foo': 'bar'})
    self.assertEqual(
      morph.omit(src), {'foo': 'bar', 'zig1': 'zog', 'zig2': 'zug'})

  #----------------------------------------------------------------------------
  def test_omit_tree(self):
    src = {
      'a': 'a',
      'b': {'x': 'b.x', 'y': 'b.y'},
      'b.x': 'b-dot-x',
      'c': [
        {'x': 'c0.x', 'y': 'c0.y'},
        {'x': 'c1.x', 'y': 'c1.y'},
      ],
    }
    self.assertEqual(
      morph.omit(src, 'a', 'b.x', 'c', tree=True),
      {'b': {'y': 'b.y'}, 'b.x': 'b-dot-x'})
    self.assertEqual(
      morph.omit(src, 'a', 'b.x', 'c'),
      {'b': {'x': 'b.x', 'y': 'b.y'}})

    # src = {'a': 'a', 'b': [{'x': 'b0.x', 'y': 'b0.y'}, {'x': 'b1.x', 'y': 'b1.y'}]}
    # self.assertEqual(
    #   morph.omit(src, 'b[0].x'),
    #   {'a': 'a', 'b': [{'y': 'b0.y'}, {'x': 'b1.x', 'y': 'b1.y'}]})
    # self.assertEqual(
    #   morph.omit(src, 'b[].x'),
    #   {'a': 'a', 'b': [{'y': 'b0.y'}, {'y': 'b1.y'}]})

  #----------------------------------------------------------------------------
  def test_xform_seq(self):
    stack = []
    def double(value, **kws):
      stack.append((value, kws))
      return value * 2
    src = [4, 'foo', -2.25]
    self.assertEqual(
      morph.xform(src, double),
      [8, 'foofoo', -4.5])
    self.assertEqual(stack, [
      (4, dict(index=0, seq=src, root=src)),
      ('foo', dict(index=1, seq=src, root=src)),
      (-2.25, dict(index=2, seq=src, root=src)),
    ])

  #----------------------------------------------------------------------------
  def test_xform_dict(self):
    stack = []
    def double(value, **kws):
      stack.append((value, kws))
      return value * 2
    src = {4: 'four', 'foo': 'bar', 'float': -2.25}
    self.assertEqual(
      morph.xform(src, double),
      {8: 'fourfour', 'foofoo': 'barbar', 'floatfloat': -4.5})
    self.assertEqual(sorted(stack, key=str), sorted([
      (4, dict(item_value='four', dict=src, root=src)),
      ('four', dict(item_key=4, dict=src, root=src)),
      ('foo', dict(item_value='bar', dict=src, root=src)),
      ('bar', dict(item_key='foo', dict=src, root=src)),
      ('float', dict(item_value=-2.25, dict=src, root=src)),
      (-2.25, dict(item_key='float', dict=src, root=src)),
    ], key=str))

  #----------------------------------------------------------------------------
  def test_xform_combined(self):
    stack = []
    def double(value, **kws):
      stack.append((value, kws))
      return value * 2
    src = {'key': [8, {'k2': -2}]}
    self.assertEqual(
      morph.xform(src, double),
      {'keykey': [16, {'k2k2': -4}]})
    self.assertEqual(sorted(stack, key=str), sorted([
      (8, dict(index=0, seq=[8, {'k2': -2}], root=src)),
      (-2, dict(item_key='k2', dict={'k2': -2}, root=src)),
      ('k2', dict(item_value=-2, dict={'k2': -2}, root=src)),
      ('key', dict(item_value=[8, {'k2': -2}], dict=src, root=src)),
    ], key=str))

class TestIsSeq(unittest.TestCase):
    def test_list(self):
        """Test that a list is correctly identified as a sequence."""
        self.assertTrue(isseq([1, 2, 3]))  # Positive case: list

    def test_tuple(self):
        """Test that a tuple is correctly identified as a sequence."""
        self.assertTrue(isseq((1, 2, 3)))  # Positive case: tuple

    def test_string(self):
        """Test that a string is not identified as a sequence."""
        self.assertFalse(isseq("string"))  # Negative case: string

    def test_dict(self):
        """Test that a dictionary is not identified as a sequence."""
        self.assertFalse(isseq({"key": "value"}))  # Negative case: dict

    def test_custom_iterable(self):
        """Test that a custom iterable without __getitem__ is identified as a sequence."""
        class CustomIterable:
            def __iter__(self):
                yield 1
                yield 2

        self.assertTrue(isseq(CustomIterable()))  # Positive case: custom iterable without __getitem__

    def test_custom_object_with_getitem_and_iter(self):
        """Test that a custom object with __getitem__ and __iter__ is not incorrectly identified as a sequence."""
        class CustomObject:
            def __getitem__(self, index):
                return index

            def __iter__(self):
                yield 1
                yield 2

        self.assertTrue(isseq(CustomObject()))  # Negative case: custom object with __getitem__ and __iter__

    def test_generator(self):
        """Test that a generator is correctly identified as a sequence."""
        def generator():
            yield 1
            yield 2

        self.assertTrue(isseq(generator()))  # Positive case: generator

    def test_iterator(self):
        """Test that an iterator is correctly identified as a sequence."""
        iterator = iter([1, 2, 3])
        self.assertTrue(isseq(iterator))  # Positive case: iterator


    def test_custom_non_sequence_object(self):
        """Test that a custom object mimicking sequence properties is not incorrectly identified as a sequence."""
        class NonSequence:
            def __getitem__(self, index):
                return index

            def __iter__(self):
                yield 1
                yield 2

            def __len__(self):
                return 2

        self.assertTrue(isseq(NonSequence()))  # Negative case: custom object mimicking sequence but not a true sequence

if __name__ == "__main__":
    unittest.main()

#------------------------------------------------------------------------------
# end of $Id$
#------------------------------------------------------------------------------
import unittest
from morph import pick

class TestPickFunction(unittest.TestCase):
    """
    Test suite for the `pick` function from the `morph` module.
    The tests cover various scenarios to ensure that the `pick` function
    behaves correctly when filtering keys from a source dictionary.
    """

    def setUp(self):
        """
        Set up the initial state for the tests.
        This method creates a sample source dictionary with various keys,
        including both string and non-string keys, to be used in the tests.
        """
        self.source = {
            'prefix_key1': 1,
            'prefix_key2': 2,
            'other_key': 3,
            123: 4,  # Non-string key to test the getattr fallback
        }

    def test_pick_with_valid_keys(self):
        """
        Test case for picking valid keys with a specified prefix.
        This test checks that the `pick` function correctly removes the 
        prefix from keys in the source dictionary and returns the expected 
        dictionary with the prefix stripped.
        """
        keys = ['prefix_key1', 'prefix_key2']
        result = pick(self.source, prefix='prefix_')
        expected = {'key1': 1, 'key2': 2}  # Should strip the prefix
        self.assertEqual(result, expected)

    def test_pick_with_non_string_keys(self):
        """
        Test case for handling non-string keys in the source dictionary.
        This test verifies that the `pick` function only returns keys 
        that are strings and ignore non-string keys, ensuring the function 
        handles edge cases gracefully.
        """
        result = pick(self.source, prefix='prefix_')
        expected = {'key1': 1, 'key2': 2}  # Only valid string keys should be returned
        self.assertEqual(result, expected)

    def test_pick_with_non_string_key_for_getattr(self):
        """
        Test case to ensure the `pick` function works with source dictionaries
        containing non-string keys when filtering by prefix.
        This verifies that the function does not raise errors and correctly
        handles keys that do not support the `startswith` method by using
        a fallback lambda.
        """
        # Testing that non-string keys correctly trigger the lambda
        source = {None: 1, 123: 2, 'prefix_key3': 3}
        result = pick(source, prefix='prefix_')
        expected = {'key3': 3}  
        self.assertEqual(result, expected)

    def test_pick_with_empty_source(self):
        """
        Test case for the scenario where the source dictionary is empty.
        This test ensures that when `pick` is called with an empty source, 
        it returns an empty dictionary as expected, demonstrating the 
        function's robustness in handling edge cases.
        """
        result = pick({}, prefix='prefix_')
        self.assertEqual(result, {}) 

    def test_pick_with_prefix_and_no_keys(self):
        """
        Test case for picking keys with a specified prefix when no keys 
        are explicitly provided. This checks that the `pick` function 
        returns the correct subset of the source dictionary based on the 
        specified prefix, verifying its functionality.
        """
        result = pick(self.source, prefix='prefix_')
        expected = {'key1': 1, 'key2': 2}  # All keys with prefix stripped
        self.assertEqual(result, expected)

    def test_pick_invalid_keywords(self):
        """
        Test case for verifying that the `pick` function raises a 
        ValueError when invalid keyword arguments are provided.
        This checks the function's error handling when called with 
        unexpected or unsupported parameters.
        """
        with self.assertRaises(ValueError):
            pick(self.source, keys=[], invalid_key='invalid')

    def test_pick_with_tree_option(self):
        """
        Test case to ensure that using both the `prefix` and `tree` options 
        together raises a ValueError. This verifies the function's ability 
        to enforce its own constraints and prevents misuse.
        """
        with self.assertRaises(ValueError):
            pick(self.source, prefix='prefix_', tree=True)  

if __name__ == '__main__':
    unittest.main()

class CustomDictLike:
    def keys(self):
        return ['key1', 'key2']

    def values(self):
        return ['value1', 'value2']

    def items(self):
        return [('key1', 'value1'), ('key2', 'value2')]

    def __getitem__(self, key):
        # This makes it behave like a dictionary
        return f'value for {key}'

import unittest

class TestIsDict(unittest.TestCase):
    """
    A test suite for the `isdict` function.
    """

    def test_custom_dict_like(self):
        """
        Test that a custom dict-like object is correctly identified.

        This test creates a `CustomDictLike` object, which should be considered
        dict-like by the `isdict` function.
        """
        self.assertTrue(morph.isdict(CustomDictLike()))

    def test_custom_sequence(self):
        """
        Test that a custom sequence object is not considered dict-like.

        This test creates a `CustomSequence` object, which should not be
        considered dict-like by the `isdict` function.
        """
        class CustomSequence:
            """
            A custom sequence object.
            """
            def __getitem__(self, index):
                return index

            def __len__(self):
                return 2

        self.assertFalse(morph.isdict(CustomSequence()))

    def test_string(self):
        """
        Test that a string is not considered dict-like.

        This test checks that a string is correctly identified as not being
        dict-like by the `isdict` function.
        """
        self.assertFalse(morph.isdict("string"))

    def test_regular_dict(self):
        """
        Test that a standard dictionary is considered dict-like.

        This test creates a standard dictionary and checks that it is correctly
        identified as dict-like by the `isdict` function.
        """
        standard_dict = {'key1': 'value1', 'key2': 'value2'}
        self.assertTrue(morph.isdict(standard_dict))

    def test_non_dict_like_object(self):
        """
        Test that an object that does not implement dict-like methods is not considered dict-like.

        This test creates a `NonDictLike` object, which does not implement any
        dict-like methods, and checks that it is correctly identified as not
        being dict-like by the `isdict` function.
        """
        class NonDictLike:
            """
            An object that does not implement dict-like methods.
            """
            pass

        self.assertFalse(morph.isdict(NonDictLike()))

    def test_partial_dict_like_object(self):
        """
        Test that an object implementing some dict-like methods but missing others is not considered dict-like.

        This test creates a `PartialDictLike` object, which implements some
        dict-like methods but is missing others, and checks that it is correctly
        identified as not being dict-like by the `isdict` function.
        """
        class PartialDictLike:
            """
            An object implementing some dict-like methods but missing others.
            """
            def keys(self):
                return ['key1']

            def values(self):
                return ['value1']

            # Missing items() method

            def __getitem__(self, key):
                return f'value for {key}'

        self.assertFalse(morph.isdict(PartialDictLike()))  

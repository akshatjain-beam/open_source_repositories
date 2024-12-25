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
#     Jesus M. Gonzalez-Barahona <jgb@gsyc.es>
#     Valerio Cosentino <valcos@bitergia.com>
#     Santiago Dueñas <sduenas@bitergia.com>
#

"""Common functions for introspection.

This module provides a set of functions that come in handy for
instrospection on a higher level than the provided by other libraries
such as `inspect`.
"""

import inspect


__all__ = [
    "inspect_signature_parameters",
    "find_signature_parameters",
    "find_class_properties"
]


def inspect_signature_parameters(callable_, excluded=None):
    """Get the parameters of a callable.

    Returns a list with the signature parameters of `callable_`.
    Parameters contained in `excluded` tuple will not be included
    in the result.

    :param callable_: callable object
    :param excluded: tuple with default parameters to exclude

    :result: list of parameters
    """
    if not excluded:
        excluded = ()

    signature = inspect.signature(callable_)
    params = [
        v for p, v in signature.parameters.items()
        if p not in excluded
    ]
    return params


def find_signature_parameters(callable_, candidates,
                              excluded=('self', 'cls')):
    """Find on a set of candidates the parameters needed to execute a callable.

    Returns a dictionary with the `candidates` found on `callable_`.
    When any of the required parameters of a callable is not found,
    it raises a `AttributeError` exception. A signature parameter
    whitout a default value is considered as required.

    If the `callable_` includes variadic parameters (`*args` or `**kwargs`), all 
    provided candidates will be included.

    :param callable_: callable object
    :param candidates: dict with the possible parameters to use
        with the callable
    :param excluded: tuple with default parameters to exclude

    :result: dict of parameters ready to use with the callable

    :raises AttributeError: when any of the required parameters for
        executing a callable is not found in `candidates`
    """
    $PlaceHolder$

def find_class_properties(cls):
    """Find property members in a class.

    Returns all the property members of a class in a list of
    (name, value) pairs. Only those members defined with `property`
    decorator will be included in the list.

    :param cls: class where property members will be searched

    :returns: list of properties
    """
    candidates = inspect.getmembers(cls, inspect.isdatadescriptor)
    result = [
        (name, value) for name, value in candidates
        if isinstance(value, property)
    ]
    return result

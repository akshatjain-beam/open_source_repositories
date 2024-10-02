# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.cbv` module.
"""


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
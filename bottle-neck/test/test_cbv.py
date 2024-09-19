# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.cbv` module.
"""


import inspect
from bottle_neck.cbv import BaseHandler


class TestBuildRoutes:
    def test_no_args(self):
        method_args = {}
        url_extra_part = None
        expected = ['/']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_single_arg(self):
        method_args = {'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None)}
        url_extra_part = None
        expected = ['/', '/:arg1']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_multiple_args(self):
        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None)
        }
        url_extra_part = None
        expected = ['/', '/:arg1', '/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_arg_with_default(self):
        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value')
        }
        url_extra_part = None
        expected = ['/:arg1']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_multiple_args_with_defaults(self):
        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value1'),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value2')
        }
        url_extra_part = None
        expected = ['/:arg1/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected

    def test_mixed_args(self):
        method_args = {
            'arg1': inspect.Parameter('arg1', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value'),
            'arg2': inspect.Parameter('arg2', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default=None),
            'arg3': inspect.Parameter('arg3', kind=inspect.Parameter.POSITIONAL_OR_KEYWORD, default='default_value')
        }
        url_extra_part = None
        expected = ['/:arg1/:arg3', '/:arg1/:arg3/:arg2']
        assert BaseHandler._build_routes(method_args, url_extra_part) == expected
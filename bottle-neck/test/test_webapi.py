# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.webapi` module.
"""

from bottle_neck.webapi import paginator


class TestPaginator:
    
    def assert_pagination_result(self, result, expected):
        for key in expected:
            assert key in result, f"Missing key in result: {key}"
            assert result[key] == expected[key], f"Key {key} - Expected: {expected[key]}, Got: {result[key]}"

    def test_first_page(self):
        result = paginator(10, 0, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=10',
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)
    
    def test_middle_page(self):
        result = paginator(10, 10, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=20',
            'prev_page': 'http://example.com/&limit=10&offset=0'
        }
        self.assert_pagination_result(result, expected)

    def test_last_page(self):
        result = paginator(10, 40, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=50',
            'prev_page': 'http://example.com/&limit=10&offset=30'
        }
        self.assert_pagination_result(result, expected)

    def test_single_page(self):
        result = paginator(50, 0, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 1,
            'next_page': 'http://example.com/&limit=50&offset=50',
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)

    def test_no_records(self):
        result = paginator(10, 0, 0, 'http://example.com/')
        expected = {
            'total_count': 0,
            'total_pages': 0,
            'next_page': None,
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)

    def test_custom_page_nav_tpl(self):
        result = paginator(10, 10, 50, 'http://example.com/', page_nav_tpl='?limit={}&offset={}')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/?limit=10&offset=20',
            'prev_page': 'http://example.com/?limit=10&offset=0'
        }
        self.assert_pagination_result(result, expected)
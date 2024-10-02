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
        """
        Test pagination for the first page of results.

        This test checks if the pagination correctly identifies the first page
        when there are records to display. The expected result includes the total
        record count, total pages, a valid next page link, and a None value for
        the previous page link.
        """
        result = paginator(10, 0, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=10',
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)
    
    def test_middle_page(self):
        """
        Test pagination for a middle page of results.

        This test verifies the pagination logic for an intermediate page. It
        ensures that both next and previous page links are generated correctly,
        with the appropriate offsets calculated based on the provided limit and offset.
        """
        result = paginator(10, 10, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=20',
            'prev_page': 'http://example.com/&limit=10&offset=0'
        }
        self.assert_pagination_result(result, expected)

    def test_last_page(self):
        """
        Test pagination for the last page of results.

        This test checks if the pagination handles the last page correctly. It
        validates that both next and previous page links are provided, with the
        correct offsets to reflect the last segment of results in the pagination.
        """
        result = paginator(10, 40, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/&limit=10&offset=50',
            'prev_page': 'http://example.com/&limit=10&offset=30'
        }
        self.assert_pagination_result(result, expected)

    def test_single_page(self):
        """
        Test pagination when the total records fit in a single page.

        This test evaluates the pagination when all records are displayed on a
        single page. The expected result should indicate that there is only one
        page, with a valid next page link that exceeds the total record count and
        a None value for the previous page.
        """
        result = paginator(50, 0, 50, 'http://example.com/')
        expected = {
            'total_count': 50,
            'total_pages': 1,
            'next_page': 'http://example.com/&limit=50&offset=50',
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)

    def test_no_records(self):
        """
        Test pagination when there are no records available.

        This test checks the pagination response when there are zero records.
        The expected result should indicate zero total records, zero total pages,
        and both next and previous page links should be None.
        """
        result = paginator(10, 0, 0, 'http://example.com/')
        expected = {
            'total_count': 0,
            'total_pages': 0,
            'next_page': None,
            'prev_page': None
        }
        self.assert_pagination_result(result, expected)

    def test_custom_page_nav_tpl(self):
        """
        Test pagination with a custom page navigation template.

        This test validates the pagination logic when a custom pagination template
        is provided. It checks if the next and previous page links are correctly
        generated using the custom template while ensuring other pagination data
        remains accurate.
        """
        result = paginator(10, 10, 50, 'http://example.com/', page_nav_tpl='?limit={}&offset={}')
        expected = {
            'total_count': 50,
            'total_pages': 5,
            'next_page': 'http://example.com/?limit=10&offset=20',
            'prev_page': 'http://example.com/?limit=10&offset=0'
        }
        self.assert_pagination_result(result, expected)
# -*- coding: utf-8 -*-
"""Bottle.py API development utilities.

Provides some extra functionality for developing web API's with `bottle.py`.
"""

from __future__ import absolute_import

__author__ = 'pav'
__date__ = '2015-2-3'
__all__ = ['cors_enable_hook', 'strip_path_hook', 'paginator']

from bottle_neck import __version__
from collections import OrderedDict
import bottle
import math

version = tuple(map(int, __version__.split('.')))


def cors_enable_hook():
    bottle.response.headers['Access-Control-Allow-Origin'] = '*'
    bottle.response.headers['Access-Control-Allow-Headers'] = \
        'Authorization, Credentials, X-Requested-With, Content-Type'
    bottle.response.headers['Access-Control-Allow-Methods'] = \
        'GET, PUT, POST, OPTIONS, DELETE'


def strip_path_hook():
    """Ignore trailing slashes.
    """
    bottle.request.environ['PATH_INFO'] = \
        bottle.request.environ['PATH_INFO'].rstrip('/')


def paginator(limit, offset, record_count, base_uri, page_nav_tpl='&limit={}&offset={}'):
    """
    Compute pagination info for collection filtering.

	Args:
	    limit (int): Collection filter limit.
	    offset (int): Collection filter offset.
	    record_count (int): Collection filter total record count.
	    base_uri (str): Collection filter base uri (without limit, offset)
	    page_nav_tpl (str): A pagination template string formatted as `&limit={}&offset={}` where the values for limit and offset need to be dynamically inserted.

	Returns:
	    A mapping of pagination info with keys `total_count`, `total_pages`, `next_page`, and `prev_page` of type `OrderedDict`

	Note:
	    The `next_page` link is provided if there are remaining records to display, including when the current page is full.
	    The `prev_page` link is provided if `offset` is greater than or equal to `limit`.
	"""
	$PlaceHolder$
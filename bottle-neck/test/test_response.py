# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.handlers` module.
"""


import pytest
import bottle_neck.response as response
from bottle_neck.response import WSResponse


def test_ws_response_init_pass():
    """Test `bottle_neck.response.WSResponse` init pass.
    """
    assert response.WSResponse(200, 1)


def test_ws_response_init_fail():
    """Test `bottle_neck.response.WSResponse` init pass.
    """
    with pytest.raises(response.WSResponseError):
        assert response.WSResponse(209, 1)


def test_ws_response_ok():
    """Test `bottle_neck.response.WSResponse.ok` method.
    """
    assert response.WSResponse.ok(data={"count": 1})


def test_ws_response_bad_request():
    """Test `bottle_neck.response.WSResponse.bad_request` method.
    """
    assert response.WSResponse.bad_request(errors=[1, 2])


def test_ws_response_created():
    """Test `bottle_neck.response.WSResponse.created` method.
    """
    assert response.WSResponse.created(data={})


def test_ws_response_not_modified():
    """Test `bottle_neck.response.WSResponse.not_modified` method.
    """
    assert response.WSResponse.not_modified()


class TestWSResponse:
    def test_from_status_200(self):
        status_line = '200 OK'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 200
        assert result['status_text'] == 'OK'
        assert result['errors'] == []

    def test_from_status_201(self):
        status_line = '201 Created'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 201
        assert result['status_text'] == 'Created'
        assert result['errors'] == []

    def test_from_status_304(self):
        status_line = '304 Not Modified'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 304
        assert result['status_text'] == 'Not Modified'
        assert result['errors'] == []

    def test_from_status_400(self):
        status_line = '400 Bad Request'
        error_msg = 'Invalid request.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 400
        assert result['status_text'] == 'Bad Request'
        assert result['errors'] == ['Invalid request.']

    def test_from_status_401(self):
        status_line = '401 Unauthorized'
        error_msg = 'Access denied.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 401
        assert result['status_text'] == 'Unauthorized'
        assert result['errors'] == ['Access denied.']

    def test_from_status_403(self):
        status_line = '403 Forbidden'
        error_msg = 'You do not have permission.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 403
        assert result['status_text'] == 'Forbidden'
        assert result['errors'] == ['You do not have permission.']

    def test_from_status_404(self):
        status_line = '404 Not Found'
        error_msg = 'Resource not found.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 404
        assert result['status_text'] == 'Not Found'
        assert result['errors'] == ['Resource not found.']

    def test_from_status_405(self):
        status_line = '405 Method Not Allowed'
        error_msg = 'Method not allowed.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 405
        assert result['status_text'] == 'Method Not Allowed'
        assert result['errors'] == ['Method not allowed.']

    def test_from_status_501(self):
        status_line = '501 Not Implemented'
        error_msg = 'Feature not implemented.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 501
        assert result['status_text'] == 'Not Implemented'
        assert result['errors'] == ['Feature not implemented.']

    def test_from_status_503(self):
        status_line = '503 Service Unavailable'
        error_msg = 'Service is down.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 503
        assert result['status_text'] == 'Service Unavailable'
        assert result['errors'] == ['Service is down.']

    def test_from_status_invalid(self):
        with pytest.raises(AttributeError):
            WSResponse.from_status('Invalid Status Line')

    def test_from_status_edge_case(self):
        status_line = '999 Unknown Status'
        with pytest.raises(AttributeError):
            WSResponse.from_status(status_line)
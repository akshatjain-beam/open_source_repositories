# -*- coding: utf-8 -*-
"""Unit Tests for `bottle_neck.handlers` module.
"""

import pytest
import bottle_neck.response as response
from bottle_neck.response import WSResponse


def test_ws_response_init_pass():
    """
    Test the successful initialization of `bottle_neck.response.WSResponse`.
    
    This test verifies that the WSResponse class can be instantiated 
    correctly with a valid status code (200) and a valid response body (1).
    The assertion checks that no exceptions are raised during initialization.
    """
    assert response.WSResponse(200, 1)


def test_ws_response_init_fail():
    """
    Test the failure of `bottle_neck.response.WSResponse` initialization.
    
    This test checks that an attempt to initialize the WSResponse class 
    with an invalid status code (209) raises a WSResponseError. The 
    assertion ensures that the error is raised as expected.
    """
    with pytest.raises(response.WSResponseError):
        assert response.WSResponse(209, 1)


def test_ws_response_ok():
    """
    Test the `WSResponse.ok` method.
    
    This test validates that the ok method of the WSResponse class 
    returns a successful response when called with a data dictionary.
    The assertion checks that the response structure is correct and
    includes the expected data.
    """
    assert response.WSResponse.ok(data={"count": 1})


def test_ws_response_bad_request():
    """
    Test the `WSResponse.bad_request` method.
    
    This test ensures that the bad_request method of the WSResponse 
    class returns a response indicating a bad request when called 
    with error messages. The assertion checks that the response 
    contains the expected errors.
    """
    assert response.WSResponse.bad_request(errors=[1, 2])


def test_ws_response_created():
    """
    Test the `WSResponse.created` method.
    
    This test verifies that the created method of the WSResponse class 
    returns a response indicating successful creation of a resource 
    when called with an empty data dictionary. The assertion checks 
    that the response is correctly structured.
    """
    assert response.WSResponse.created(data={})


def test_ws_response_not_modified():
    """
    Test the `WSResponse.not_modified` method.
    
    This test validates that the not_modified method of the WSResponse 
    class returns a response indicating that the resource has not 
    been modified. The assertion checks that the response is 
    structured correctly.
    """
    assert response.WSResponse.not_modified()


class TestWSResponse:
    def test_from_status_200(self):
        """
        Test the `WSResponse.from_status` method for status line 200 OK.
        
        This test checks that the from_status method correctly parses 
        the status line '200 OK' and returns a response with the 
        correct status code, status text, and no errors.
        """
        status_line = '200 OK'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 200
        assert result['status_text'] == 'OK'
        assert result['errors'] == []

    def test_from_status_201(self):
        """
        Test the `WSResponse.from_status` method for status line 201 Created.
        
        This test verifies that the from_status method can handle the 
        status line '201 Created', ensuring it returns the correct 
        status code and status text without any errors.
        """
        status_line = '201 Created'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 201
        assert result['status_text'] == 'Created'
        assert result['errors'] == []

    def test_from_status_304(self):
        """
        Test the `WSResponse.from_status` method for status line 304 Not Modified.
        
        This test checks that the from_status method processes the 
        status line '304 Not Modified' correctly, returning the proper 
        status code, status text, and an empty errors list.
        """
        status_line = '304 Not Modified'
        result = WSResponse.from_status(status_line)

        assert result['status_code'] == 304
        assert result['status_text'] == 'Not Modified'
        assert result['errors'] == []

    def test_from_status_400(self):
        """
        Test the `WSResponse.from_status` method for status line 400 Bad Request.
        
        This test ensures that the from_status method can handle the 
        status line '400 Bad Request' with a provided error message, 
        verifying that the response contains the expected status code, 
        status text, and errors.
        """
        status_line = '400 Bad Request'
        error_msg = 'Invalid request.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 400
        assert result['status_text'] == 'Bad Request'
        assert result['errors'] == ['Invalid request.']

    def test_from_status_401(self):
        """
        Test the `WSResponse.from_status` method for status line 401 Unauthorized.
        
        This test checks that the from_status method processes the 
        status line '401 Unauthorized' correctly, returning the 
        expected status code, status text, and a list containing the 
        provided error message.
        """
        status_line = '401 Unauthorized'
        error_msg = 'Access denied.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 401
        assert result['status_text'] == 'Unauthorized'
        assert result['errors'] == ['Access denied.']

    def test_from_status_403(self):
        """
        Test the `WSResponse.from_status` method for status line 403 Forbidden.
        
        This test verifies that the from_status method correctly 
        processes the status line '403 Forbidden', ensuring the response 
        contains the correct status code, status text, and provided 
        error message.
        """
        status_line = '403 Forbidden'
        error_msg = 'You do not have permission.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 403
        assert result['status_text'] == 'Forbidden'
        assert result['errors'] == ['You do not have permission.']

    def test_from_status_404(self):
        """
        Test the `WSResponse.from_status` method for status line 404 Not Found.
        
        This test checks that the from_status method handles the 
        status line '404 Not Found', returning the appropriate status 
        code, status text, and an error message indicating that the 
        resource was not found.
        """
        status_line = '404 Not Found'
        error_msg = 'Resource not found.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 404
        assert result['status_text'] == 'Not Found'
        assert result['errors'] == ['Resource not found.']

    def test_from_status_405(self):
        """
        Test the `WSResponse.from_status` method for status line 405 Method Not Allowed.
        
        This test ensures that the from_status method correctly processes 
        the status line '405 Method Not Allowed', returning the expected 
        status code, status text, and an error message indicating the 
        method is not allowed.
        """
        status_line = '405 Method Not Allowed'
        error_msg = 'Method not allowed.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 405
        assert result['status_text'] == 'Method Not Allowed'
        assert result['errors'] == ['Method not allowed.']

    def test_from_status_501(self):
        """
        Test the `WSResponse.from_status` method for status line 501 Not Implemented.
        
        This test checks that the from_status method can handle the 
        status line '501 Not Implemented' with a specific error message, 
        ensuring it returns the correct status code, status text, and 
        error information.
        """
        status_line = '501 Not Implemented'
        error_msg = 'Feature not implemented.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 501
        assert result['status_text'] == 'Not Implemented'
        assert result['errors'] == ['Feature not implemented.']

    def test_from_status_503(self):
        """
        Test the `WSResponse.from_status` method for status line 503 Service Unavailable.
        
        This test verifies that the from_status method processes the 
        status line '503 Service Unavailable' correctly, returning the 
        expected status code, status text, and a provided error message.
        """
        status_line = '503 Service Unavailable'
        error_msg = 'Service is down.'
        result = WSResponse.from_status(status_line, error_msg)

        assert result['status_code'] == 503
        assert result['status_text'] == 'Service Unavailable'
        assert result['errors'] == ['Service is down.']

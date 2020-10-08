# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        create user on emulab testbed
        """
        body = User()
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/ericafu1122/aerpawgateway/1.0.0/user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        delete user
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/ericafu1122/aerpawgateway/1.0.0/user',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_user(self):
        """Test case for get_user

        get user information
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/ericafu1122/aerpawgateway/1.0.0/user',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

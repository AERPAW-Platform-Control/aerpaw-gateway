# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProfileController(BaseTestCase):
    """ProfileController integration test stubs"""

    def test_create_profile(self):
        """Test case for create_profile

        create profile
        """
        body = Profile()
        response = self.client.open(
            '/aerpawgateway/1.0.0/profile',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_profile(self):
        """Test case for delete_profile

        delete profile
        """
        query_string = [('username', 'username_example'),
                        ('project', 'project_example'),
                        ('name', 'name_example')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/profile',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profile(self):
        """Test case for get_profile

        get profiles under user
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/profile',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

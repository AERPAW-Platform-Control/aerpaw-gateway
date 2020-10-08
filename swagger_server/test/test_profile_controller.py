# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server.test import BaseTestCase


class TestProfileController(BaseTestCase):
    """ProfileController integration test stubs"""

    def test_get_profile(self):
        """Test case for get_profile

        get profiles under user
        """
        query_string = [('username', 'username_example')]
        response = self.client.open(
            '/ericafu1122/aerpawgateway/1.0.0/profile',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

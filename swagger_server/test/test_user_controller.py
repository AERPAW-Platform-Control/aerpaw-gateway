# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.userkey import Userkey  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_adduser(self):
        """Test case for adduser

        add/update user and sshkey on experiment nodes
        """
        body = Userkey()
        query_string = [('experiment', 'experiment_example'),
                        ('project', 'project_example')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/user',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

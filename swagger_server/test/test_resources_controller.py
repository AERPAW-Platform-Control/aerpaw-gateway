# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server.test import BaseTestCase


class TestResourcesController(BaseTestCase):
    """ResourcesController integration test stubs"""

    def test_list_resources(self):
        """Test case for list_resources

        list resources
        """
        query_string = [('username', 'erikaadm'),
                        ('project', 'TestProject1'),
                        ('experiment', 'aerpaw001')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/resources',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.reservation import Reservation  # noqa: E501
from swagger_server.test import BaseTestCase


class TestReservationController(BaseTestCase):
    """ReservationController integration test stubs"""

    def test_create_reservation(self):
        """Test case for create_reservation

        create reservation
        """
        body = Reservation()
        query_string = [('validate', true)]
        response = self.client.open(
            '/aerpawgateway/1.0.0/reservation',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_reservation(self):
        """Test case for delete_reservation

        delete reservation
        """
        query_string = [('username', 'username_example'),
                        ('cluster', 'cluster_example'),
                        ('project', 'project_example'),
                        ('reservation', 'reservation_example')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/reservation',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_reservation(self):
        """Test case for get_reservation

        get reservation under user
        """
        query_string = [('username', 'username_example'),
                        ('cluster', 'cluster_example')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/reservation',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

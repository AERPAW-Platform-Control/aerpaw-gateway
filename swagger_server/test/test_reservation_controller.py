# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.reservation import Reservation  # noqa: E501
from swagger_server.test import BaseTestCase
from datetime import datetime


class TestReservationController(BaseTestCase):
    """ReservationController integration test stubs"""

    def test_create_reservation(self):
        """Test case for create_reservation

        create reservation
        """
        start = int(datetime.utcnow().timestamp())
        end = start + 60 * 60 * 10  # 10 hours
        body = Reservation(cluster='RENCI', experiment='aerpaw-unittest', nodes=1,
                           project='TestProject1', start=str(start), end=str(end), type='x3651',
                           username='erikafu')
        query_string = [('validate', 'false')]
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
        query_string = [('username', 'erikafu'),
                        ('cluster', 'RENCI'),
                        ('project', 'TestProject1'),
                        ('reservation', '160ff144-2523-11eb-a596-6cae8b3bf14a')]
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
        query_string = [('username', 'erikafu'),
                        ('cluster', 'RENCI')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/reservation',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

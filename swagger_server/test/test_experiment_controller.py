# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server.test import BaseTestCase
from datetime import datetime
import time


class TestExperimentController(BaseTestCase):
    """ExperimentController integration test stubs"""

    def test_create_experiment(self):
        """Test case for create_experiment

        create a experiment
        """
        start = int(datetime.utcnow().timestamp())
        end = start + 60*60*10  # 10 hours
        body = Experiment(cluster='RENCI', name='aerpaw-unittest', username='erikafu',
                          project='TestProject1', profile='TestProject1,aerpaw-unittest',
                          start=str(start), end=str(end))
        response = self.client.open(
            '/aerpawgateway/1.0.0/experiment',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        time.sleep(60*3)  # allow experiment to be created

    def test_get_experiments(self):
        """Test case for get_experiments

        get experiment(s) under user
        """
        query_string = [('username', 'erikafu')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/experiments',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_query_experiment(self):
        """Test case for query_experiment

        get status of specific experiment
        """
        query_string = [('username', 'erikafu'),
                        ('project', 'TestProject1')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/experiment/{experiment}'.format(experiment='aerpaw-unittest'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_experiment(self):
        """Test case for delete_experiment

        delete experiment
        """
        query_string = [('username', 'erikafu'),
                        ('project', 'TestProject1'),
                        ('experiment', 'aerpaw-unittest')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/experiment',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))
        time.sleep(30)  # allow experiment to be deleted


if __name__ == '__main__':
    import unittest
    unittest.main()

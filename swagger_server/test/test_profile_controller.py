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
        body = Profile(creator='erikafu', name='unittest', project='TestProject1',
                       script="\"\"\"One raw PC running the default OS.\n\nInstructions:\nLog into your PC and poke around. You have root access via `sudo`. Any work you do on your PC will be lost when it terminates.\"\"\"\n\n# Import the Portal object.\nimport geni.portal as portal\n# Import the ProtoGENI library.\nimport geni.rspec.pg as pg\n# Import the Emulab specific extensions.\nimport geni.rspec.emulab as emulab\n\n# Create a portal object,\npc = portal.Context()\n\n# Create a Request object to start building the RSpec.\nrequest = pc.makeRequestRSpec()\n\n# Node node1\nnode1 = request.RawPC('node1')\n\n# Print the generated rspec\npc.printRequestRSpec(request)\n")
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
        query_string = [('username', 'erikafu'),
                        ('project', 'TestProject1'),
                        ('name', 'unittest')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/profile',
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_profiles(self):
        """Test case for get_profiles

        get profiles under user
        """
        query_string = [('username', 'erikafu')]
        response = self.client.open(
            '/aerpawgateway/1.0.0/profiles',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server import util
from . import emulab
import json
import os


def create_profile(body):  # noqa: E501
    """create profile

    Create Profile # noqa: E501

    :param body: Profile Object
    :type body: dict | bytes

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        req = Profile.from_dict(connexion.request.get_json())  # noqa: E501
    xmlfile = emulab.create_profile_xml(req.project, req.name, req.script)
    xmlpath = emulab.send_file(xmlfile)

    emulab_cmd = '{} sudo -u {} manage_profile create {}'.format(
                emulab.SSH_CMD, req.creator, xmlpath)
    emulab.send_request(emulab_cmd)

    # clean up the temporary files
    os.unlink(xmlfile)
    emulab_cmd = '{} rm {}'.format(emulab.SSH_CMD, xmlpath)
    emulab.send_request(emulab_cmd)

    response = ApiResponse(code=0,
                           output="Please use getProfile to check whether success or fail")
    return response


def delete_profile(username, project, name):  # noqa: E501
    """delete profile

    delete profile # noqa: E501

    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str
    :param name: name of profile to delete
    :type name: str

    :rtype: None
    """
    emulab_cmd = '{} sudo -u {} manage_profile delete {},{}'.format(
        emulab.SSH_CMD, username, project, name)
    emulab.send_request(emulab_cmd)
    response = ApiResponse(code=0,
                           output="Please use getProfile to check whether success or fail")
    return response


def get_profile(username):  # noqa: E501
    """get profiles under user

    get profiles under user # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: List[Profile]
    """
    emulab_cmd = '{} python ~/aerpaw/querydb.py {} list_profiles'.format(emulab.SSH_CMD, username)
    emulab_stdout = emulab.send_request(emulab_cmd)
    profiles = []
    if emulab_stdout:
        results = json.loads(emulab_stdout)
        print(results)
        for record in results:
            for k in list(record):
                if not getattr(Profile, k, None):
                    print(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            profile = Profile(**record)
            profiles.append(profile)

    return profiles

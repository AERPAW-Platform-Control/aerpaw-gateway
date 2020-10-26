import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server import util
from . import emulab
import json

def create_profile(body):  # noqa: E501
    """create profile

    Create Profile # noqa: E501

    :param body: Profile Object
    :type body: dict | bytes

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        body = Profile.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


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
    return 'do some magic!'


def get_profile(username):  # noqa: E501
    """get profiles under user

    get profiles under user # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: List[Profile]
    """
    emulab_cmd = '{} python ~/aerpaw/querydb.py {} list_profiles'.format(emulab.CMD_PREFIX, username)
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

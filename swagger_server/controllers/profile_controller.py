import connexion
import six

from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server import util
from . import emulab
import json

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

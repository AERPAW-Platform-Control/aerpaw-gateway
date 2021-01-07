import connexion
import six

from swagger_server.models.userkey import Userkey  # noqa: E501
from swagger_server import util


def adduser(body, experiment, project=None):  # noqa: E501
    """add/update user and sshkey on experiment nodes

     # noqa: E501

    :param body: User Object
    :type body: dict | bytes
    :param experiment: experiment for the request
    :type experiment: str
    :param project: project of the experiment
    :type project: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = Userkey.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


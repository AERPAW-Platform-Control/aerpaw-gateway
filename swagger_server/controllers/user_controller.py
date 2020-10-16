import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server.models.user import User  # noqa: E501
from swagger_server import util


def create_user(body, username):  # noqa: E501
    """create user on emulab testbed

     # noqa: E501

    :param body: User Object
    :type body: dict | bytes
    :param username: username for the request
    :type username: str

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_user(username):  # noqa: E501
    """delete user

     # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: None
    """
    return 'do some magic!'


def get_user(username):  # noqa: E501
    """get user information

    get user information # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: List[Experiment]
    """
    return 'do some magic!'

import connexion
import six

from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server import util


def get_profile(username):  # noqa: E501
    """get profiles under user

    get profiles under user # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: List[Experiment]
    """
    return 'do some magic!'

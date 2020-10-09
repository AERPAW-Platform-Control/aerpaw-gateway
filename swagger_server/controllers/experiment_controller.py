import connexion
import six

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server import util
from . import emulab


def create_experiment(body):  # noqa: E501
    """ceate a experiment

    instantiate/start experiment # noqa: E501

    :param body: Reservation Object
    :type body: dict | bytes

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        req = Experiment.from_dict(connexion.request.get_json())  # noqa: E501

    emulab_cmd = '{} sudo -u {} start-experiment -a {} -w --name {} --project {} {}'.format(
        emulab.CMD_PREFIX, req.username, req.cluster, req.experiment, req.project, req.profile)
    emulab_stdout = emulab.send_request(emulab_cmd)
    print(emulab_stdout)
    return ApiResponse(code=0, output="Please use getExperiment to check whether success or fail")


def delete_experiment(username, project, experiment, cluster=None):  # noqa: E501
    """delete experiment

    delete/terminate experiment # noqa: E501

    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str
    :param experiment: experiment to delete
    :type experiment: int
    :param cluster: either cluster name or cluster_urn
    :type cluster: str

    :rtype: None
    """
    return 'do some magic!'


def get_experiments(username, cluster=None):  # noqa: E501
    """get experiment(s) under user

    get experiment(s) under user # noqa: E501

    :param username: username for the request
    :type username: str
    :param cluster: either cluster name or cluster_urn
    :type cluster: str

    :rtype: List[Experiment]
    """
    return 'do some magic!'


def query_experiment(username, project, experiment, cluster=None):  # noqa: E501
    """get status of specific experiment

    get Experiment status of specific experiment # noqa: E501

    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str
    :param experiment: experiment name to query
    :type experiment: str
    :param cluster: either cluster name or cluster_urn
    :type cluster: str

    :rtype: List[Experiment]
    """
    emulab_cmd = '{} sudo -u {} manage_instance status {},{}'.format(
        emulab.CMD_PREFIX, username, project, experiment)
    emulab_stdout = emulab.send_request(emulab_cmd)
    print(emulab_stdout)
    return None


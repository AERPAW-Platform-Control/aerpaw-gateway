import connexion
import six
import os

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server import util
from . import emulab
import json


def create_experiment(body):  # noqa: E501
    """create a experiment

    instantiate/start experiment # noqa: E501

    :param body: Reservation Object
    :type body: dict | bytes

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        req = Experiment.from_dict(connexion.request.get_json())  # noqa: E501

    urn = req.cluster
    if 'urn' not in urn:
        urn = os.getenv('URN_' + req.cluster)
    print(urn)

    emulab_cmd = '{} sudo -u {} start-experiment -a {} -w --name {} --project {} {}'.format(
        emulab.CMD_PREFIX, req.username, urn, req.experiment, req.project, req.profile)
    emulab_stdout = emulab.send_request(emulab_cmd)
    print(emulab_stdout)
    return ApiResponse(code=0, output="Please use getExperiment to check whether success or fail")


def delete_experiment(username, project, experiment):  # noqa: E501
    """delete experiment

    delete/terminate experiment # noqa: E501

    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str
    :param experiment: experiment to delete
    :type experiment: int
    :type experiment: str

    :rtype: None
    """
    emulab_cmd = '{} sudo -u {} manage_instance terminate {},{}'.format(
        emulab.CMD_PREFIX, username, project, experiment)
    emulab_stdout = emulab.send_request(emulab_cmd)
    print(emulab_stdout)
    return 'OK'


def get_experiments(username, cluster=None):  # noqa: E501
    """get experiment(s) under user

    get experiment(s) under user # noqa: E501

    :param username: username for the request
    :type username: str
    :param cluster: either cluster name or cluster_urn
    :type cluster: str

    :rtype: List[Experiment]
    """

    emulab_cmd = '{} python ~/aerpaw/list_experiments.py {}'.format(emulab.CMD_PREFIX, username)
    emulab_stdout = emulab.send_request(emulab_cmd)
    experiments = []
    if emulab_stdout:
        results = json.loads(emulab_stdout)
        print(results)
        for record in results:
            record['experiment'] = record.pop('name')
            # print(reservation)
            for k in list(record):
                if not getattr(Experiment, k, None):
                    print(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            experiment = Experiment(**record)
            experiments.append(experiment)

    return experiments


def query_experiment(username, project, experiment):  # noqa: E501
    """get status of specific experiment

    get Experiment status of specific experiment # noqa: E501

    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str
    :param experiment: experiment name to query
    :type experiment: str

    :rtype: List[Experiment]
    """
    emulab_cmd = '{} sudo -u {} manage_instance status {},{}'.format(
        emulab.CMD_PREFIX, username, project, experiment)
    emulab_stdout = emulab.send_request(emulab_cmd)
    # example of output: b'Status: ready\nUUID: dc6df64d-0ef9-11eb-9b1f-6cae8b3bf14a\nwbstore: dd41e11e-0ef9-11eb-9b1f-6cae8b3bf14a\n'
    results = dict(item.split(': ') for item in emulab_stdout.decode('utf-8').split('\n', 2))
    experiment = Experiment(experiment=experiment, project=project,
                            status=results['Status'], uuid=results['UUID'])
    print(results)
    return experiment


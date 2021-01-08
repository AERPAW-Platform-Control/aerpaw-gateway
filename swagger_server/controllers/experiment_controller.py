import connexion
import six
import os
from flask import abort
from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.experiment import Experiment  # noqa: E501
from swagger_server import util
from . import emulab
import json
import logging

logger = logging.getLogger(__name__)


def create_experiment(body):  # noqa: E501
    """create a experiment

    instantiate/start experiment # noqa: E501

    :param body: Experiment Object
    :type body: dict | bytes

    :rtype: ApiResponse
    """
    if connexion.request.is_json:
        req = Experiment.from_dict(connexion.request.get_json())  # noqa: E501

    urn = req.cluster
    if 'urn' not in urn:
        urn = os.getenv('URN_' + req.cluster)
    elif 'authority+cm' not in urn:
        urn = urn + '+authority+cm'
    logger.info('urn = {}'.format(urn))

    if ',' not in req.profile:
        req.profile = emulab.EMULAB_PROJ + ',' + req.profile

    if req.username is None:
        req.username = emulab.EMULAB_USER
    if req.project is None:
        req.project = emulab.EMULAB_PROJ

    emulab_cmd = '{} sudo -u {} start-experiment -a {} -w --name {} --project {} {}'.format(
        emulab.SSH_BOSS, req.username, urn, req.name, req.project, req.profile)
    emulab_stdout = emulab.send_request(emulab_cmd)
    return ApiResponse(code=0, output="Please use getExperiment to check whether success or fail")


def delete_experiment(experiment, username=None, project=None):  # noqa: E501
    """delete experiment

    delete/terminate experiment # noqa: E501

    :param experiment: experiment to delete
    :type experiment: str
    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str

    :rtype: None
    """
    if username is None:
        username = emulab.EMULAB_USER
    if project is None:
        project = emulab.EMULAB_PROJ

    emulab_cmd = '{} sudo -u {} manage_instance terminate {},{}'.format(
        emulab.SSH_BOSS, username, project, experiment)
    emulab_stdout = emulab.send_request(emulab_cmd)
    return 'OK'


def get_experiments(username=None):  # noqa: E501
    """get experiment(s) under user

    get experiment(s) under user # noqa: E501

    :param username: username for the request
    :type username: str

    :rtype: List[Experiment]
    """

    if username is None:
        username = emulab.EMULAB_USER

    emulab_cmd = '{} sudo python /root/aerpaw/querydb.py {} list_experiments'.format(emulab.SSH_BOSS, username)
    emulab_stdout = emulab.send_request(emulab_cmd)
    experiments = []
    if emulab_stdout:
        results = json.loads(emulab_stdout)
        logger.info(results)
        for record in results:
            for k in list(record):
                if not getattr(Experiment, k, None):
                    logger.info(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            experiment = Experiment(**record)
            experiments.append(experiment)

    return experiments


def query_experiment(experiment, username=None, project=None):  # noqa: E501
    """get status of specific experiment

    get Experiment status of specific experiment # noqa: E501

    :param experiment: experiment name to query
    :type experiment: str
    :param username: username for the request
    :type username: str
    :param project: project name
    :type project: str

    :rtype: Experiment
    """

    if username is None:
        username = emulab.EMULAB_USER
    if project is None:
        project = emulab.EMULAB_PROJ

    emulab_cmd = '{} sudo -u {} manage_instance status {},{}'.format(
        emulab.SSH_BOSS, username, project, experiment)
    emulab_stdout = emulab.send_request(emulab_cmd)
    # example of output: b'Status: ready\nUUID: dc6df64d-0ef9-11eb-9b1f-6cae8b3bf14a\nwbstore: dd41e11e-0ef9-11eb-9b1f-6cae8b3bf14a\n'
    if len(emulab_stdout) == 0 or emulab_stdout.decode('utf-8').find('Status') < 0:
        abort(404, description="No such instance")

    results = dict(item.split(': ') for item in emulab_stdout.decode('utf-8').split('\n', 2))
    experiment = Experiment(name=experiment, project=project,
                            status=results['Status'], uuid=results['UUID'])
    logger.info(results)
    return experiment



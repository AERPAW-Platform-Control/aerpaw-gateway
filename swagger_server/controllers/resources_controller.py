import connexion
import six

from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server import util
import os
from flask import abort
from . import emulab
import geni.util
import geni.aggregate.cloudlab
import geni.aggregate.pgutil as ProtoGENI
import logging

logger = logging.getLogger(__name__)


def list_resources(username=None, project=None, experiment=None):  # noqa: E501
    """list resources

    List resources # noqa: E501

    :param username: The username for the request
    :type username: str
    :param project: Project pid
    :type project: str
    :param experiment: if experiment id is given, manifest rspec of the experiment will be returned.
    :type experiment: str

    :rtype: Resource
    """
    context = geni.util.loadContext(key_passphrase=os.getenv('EMULAB_PASSWORD'))
    logger.debug(context.cf.key)
    logger.debug(context.cf.cert)
    try:
        emulab.maybe_renew_genicred()  # renew credential every 24 hour
        if project and experiment:
            logger.info('query manifest for experiment')
            urn = 'urn:publicid:IDN+exogeni.net:{}+slice+{}'.format(project, experiment)
            logger.info('urn = {}'.format(urn))
            ad = geni.aggregate.cloudlab.Renci.listresources(context, urn)
            vnodes = emulab.parse_manifest(ad)
            resources = Resource(rspec=ad.text, vnodes=vnodes)
            logger.info(resources)
        else:
            logger.info('list resources')
            ad = geni.aggregate.cloudlab.Renci.listresources(context)
            reservable = emulab.get_reservable_nodes(ad)
            resources = Resource(rspec=ad.text, nodes=reservable)
    except ProtoGENI.AMError as err:
        abort(400, description=err.text)
    return resources


""" use ssh command instead of geni-lib
def list_resources(username=None, project=None, experiment=None):  # noqa: E501

    emulab_cmd = '{} sudo -u {} /usr/testbed/libexec/ptopgen -x -g 2 -r -f'.format(emulab.CMD_PREFIX, username)
    emulab_cmd_args = shlex.split(emulab_cmd)
    try:
        emulab_stdout = subprocess.check_output(emulab_cmd_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        abort(500)

    return emulab_stdout
"""

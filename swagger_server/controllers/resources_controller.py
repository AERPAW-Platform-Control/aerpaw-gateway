import connexion
import six

from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server.models.resource import Resource  # noqa: E501
from swagger_server.models.vnode import Vnode  # noqa: F401,E501
from swagger_server import util
import os
from flask import abort
from . import emulab
import geni.util
import geni.aggregate.cloudlab
import geni.aggregate.pgutil as ProtoGENI
import logging
import tempfile, os, subprocess
import xml.etree.ElementTree as ET

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
        if experiment:

            # we can use either way, geni-lib or boss command
            # rspec = experiment_controller.dumpmanifest_experiment(experiment)
            if project is None:
                project = emulab.EMULAB_PROJ
            logger.info('query manifest for experiment')
            urn = 'urn:publicid:IDN+exogeni.net:{}+slice+{}'.format(project, experiment)
            logger.info('urn = {}'.format(urn))
            ad = geni.aggregate.cloudlab.Renci.listresources(context, urn)
            logger.info(ad.text)
            rspec = ad.text
            vnodes = emulab.parse_manifest(rspec=rspec)

            resources = Resource(rspec=rspec, vnodes=vnodes)
            logger.info(vnodes)
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

def parse_resources(body):  # noqa: E501
    """Parse resources

    Parse resources # noqa: E501

    :param body: Profile Object
    :type body: dict | bytes

    :rtype: Resource
    """
    if connexion.request.is_json:
        profile = Profile.from_dict(connexion.request.get_json())  # noqa: E501
        script = profile.script
    else:
        abort(405, "Invalid input")

    if script is "":
        abort(405, "No script is provided")

    fd, path = tempfile.mkstemp(suffix='.py')
    with open(path, 'w') as f:
        f.write(script)
    # with open(path, 'r') as f:
    #    print(f.read())
    cmd = 'python {}'.format(path)
    rspec = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True).decode()
    logger.info(rspec)
    os.unlink(path)

    return parse_rspec_profile(rspec=rspec)


def parse_rspec_profile(rspec):
    try:
        root = ET.fromstring(rspec)
        nodes = root.findall(".//{http://www.geni.net/resources/rspec/3}node")
        vnodes = []
        for node in nodes:
            client_id = node.attrib['client_id'] # eg. 'node1'
            if 'component_id' in node.attrib:
                component_id = node.attrib['component_id']
            else:
                component_id = ''

            element_hardware_type = node.find(".//{http://www.geni.net/resources/rspec/3}hardware_type")
            if element_hardware_type is None:
                hardware_type = ''
            else:
                hardware_type = element_hardware_type.attrib['name']

            element_sliver_type = node.find(".//{http://www.geni.net/resources/rspec/3}sliver_type")
            sliver_type = element_sliver_type.attrib['name']
            element_disk_image = element_sliver_type.find(".//{http://www.geni.net/resources/rspec/3}disk_image")
            if element_disk_image is None:
                disk_image = ''
            else:
                disk_image = element_disk_image.attrib['name']

            newnode = Vnode(name=client_id,                         # 'node1'
                            node=component_id,                      # 'CC1' or 'CC2'
                            type=sliver_type,                       # 'raw' or 'raw-pc'
                            hardware_type=hardware_type,            # 'FixedNode'
                            disk_image=disk_image)                  # 'UBUNTU20-64-STD'

            vnodes.append(newnode)
            logger.info(newnode)
        resources = Resource(rspec=rspec, vnodes=vnodes)
    except:
        abort(400, description='exception occured while parsing rspec profile')

    return resources



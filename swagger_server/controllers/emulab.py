import subprocess
import tempfile
import os
import shlex
from flask import abort
import xml.etree.ElementTree as ET
import geni.util
import geni.aggregate.cloudlab
import geni.aggregate.pgutil
import time
from swagger_server.models.node import Node  # noqa: F401,E501
from swagger_server.models.vnode import Vnode  # noqa: F401,E501
from pathlib import Path
import logging

PARSE_PL_FILE = os.getenv('PARSE_PL_FILE')
BOSS_HOST = os.getenv('BOSS_HOST')
EMULAB_USER = os.getenv('EMULAB_USER')
EMULAB_PROJ = os.getenv('EMULAB_PROJ')
SSH_KEY = '~/.ssh/id_rsa'
SCP_CMD = 'scp -i {}'.format(SSH_KEY)
SSH_STR = 'ssh -i {} -o StrictHostKeyChecking=no'.format(SSH_KEY)
SSH_BOSS = '{} {}@{}'.format(SSH_STR, EMULAB_USER, BOSS_HOST)
usercred_file = '{}/.bssw/geni/emulab-ch2-{}-usercred.xml'.format(str(Path.home()), EMULAB_USER)
logger = logging.getLogger(__name__)


def send_request(emulab_cmd):
    """send_request
        issue emulab cmd to boss machine of emulab

        :param emulab_cmd: string type
        :rtype: emulab stdout, string type
    """

    logger.info(emulab_cmd)
    try:
        proc = subprocess.Popen(emulab_cmd, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        logger.info(stdout)
        logger.info(stderr)
        logger.info('return code = {}'.format(proc.returncode))
    except subprocess.CalledProcessError as err:
        proc.returncode = 1
        stderr = err.output

    if proc.returncode is not 0:
        logger.warning(stderr)
        if b'Profile does not exist' in stderr:
            abort(404, description="Profile does not exist")
        elif b'unknown user' in stderr:
            abort(404, description="Unknown user")
        elif b'No such project' in stderr:
            abort(404, description="No such project")
        elif b'No such instance' in stderr:
            abort(404, description="No such instance")
        elif b'Search Failed' in stderr:
            abort(404, description="Search Failed")
        elif b'Experiment name already in use' in stderr:
            abort(400, description="Experiment name already in use")
        elif b'profile_name: Already in use' in stdout:
            abort(404, description="profile_name: Already in use")
        elif len(stdout) > 0:
            abort(500, description=stdout.decode("utf-8"))
        else:
            abort(500, description=stderr.decode("utf-8"))

    return stdout


def parse_response(emulab_output):
    """parse_response
        Parse emulab perl output to json string

        :param emulab_output: string type
        :rtype: json_string
    """
    logger.info(emulab_output)
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(emulab_output)
    fp.close()
    try:
        json_string = subprocess.check_output([PARSE_PL_FILE, fp.name],
                                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        os.unlink(fp.name)
        logger.warning(err.output)
        return err.output

    os.unlink(fp.name)
    logger.info(json_string)
    return json_string


def create_profile_xml(profile_pid, profile_name, script, profile_listed='1', profile_public='1'):
    """create_profile_xml

        Create XML file for creating profile in Emulab # noqa: E501

        :param profile_pid: string type
        :param profile_name: string type
        :param script: string type
        :param profile_listed: string type
        :param profile_public: string type

        :rtype: filename of the generated temporary file
    """

    # generate rspec from script
    """
    if script is None:
        script = open('/Users/ericafu/Documents/Github/aerpaw-gateway/testonepc.py').read()
        # abort(404, description="script is empty")
    """
    fp_script = tempfile.NamedTemporaryFile(delete=False)
    fp_script.write(script.encode())
    logger.debug(script.encode())
    fp_script.close()
    rspec = subprocess.check_output(["python3", fp_script.name])
    logger.debug(rspec.decode('utf-8'))
    os.unlink(fp_script.name)

    # prepare XML
    profile = ET.Element('profile')

    profile_pid_attr = ET.SubElement(profile, 'attribute')
    profile_pid_attr.set('name', 'profile_pid')
    profile_pid_value = ET.SubElement(profile_pid_attr, 'value')
    profile_pid_value.text = profile_pid

    profile_name_attr = ET.SubElement(profile, 'attribute')
    profile_name_attr.set('name', 'profile_name')
    profile_name_value = ET.SubElement(profile_name_attr, 'value')
    profile_name_value.text = profile_name

    rspec_attr = ET.SubElement(profile, 'attribute')
    rspec_attr.set('name', 'rspec')
    rspec_value = ET.SubElement(rspec_attr, 'value')
    rspec_value.text = rspec.decode('utf-8')

    script_attr = ET.SubElement(profile, 'attribute')
    script_attr.set('name', 'script')
    script_value = ET.SubElement(script_attr, 'value')
    script_value.text = script

    profile_listed_attr = ET.SubElement(profile, 'attribute')
    profile_listed_attr.set('name', 'profile_listed')
    profile_listed_value = ET.SubElement(profile_listed_attr, 'value')
    profile_listed_value.text = profile_listed

    profile_public_attr = ET.SubElement(profile, 'attribute')
    profile_public_attr.set('name', 'profile_public')
    profile_public_value = ET.SubElement(profile_public_attr, 'value')
    profile_public_value.text = profile_public

    xmldata = ET.tostring(profile)
    logger.debug(xmldata)

    xmltmpfile = tempfile.NamedTemporaryFile(delete=False)
    xmltmpfile.write(xmldata)
    xmltmpfile.close()

    subprocess.check_output(['chmod', '644', xmltmpfile.name], stderr=subprocess.STDOUT)

    return xmltmpfile.name


def send_file(filepath):
    """send_file
        issue scp to copy input file to boss machine of emulab

        :param filepath: string type
        :rtype: xml path in boss
    """
    logger.info('filepath = {}'.format(filepath))
    scp_args = shlex.split('{} {} {}@{}:/tmp/'.format(SCP_CMD, filepath, EMULAB_USER, BOSS_HOST))
    # ssh_args = shlex.split('{} chmod 644 /tmp/{}'.format(SSH_BOSS, os.path.basename(filepath)))
    try:
        subprocess.check_output(scp_args, stderr=subprocess.STDOUT)
        # subprocess.check_output(ssh_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        logger.warning(err.output)
        abort(500, description=err.output.decode("utf-8"))
    return '/tmp/{}'.format(os.path.basename(filepath))


def maybe_renew_genicred():
    if os.path.exists(usercred_file):
        elapsed = time.time() - maybe_renew_genicred.timestamp
        logger.info('last renew time of cred xml: {}'.format(
            time.asctime(time.localtime(maybe_renew_genicred.timestamp))))
        if elapsed > 24 * 60 * 55:  # the credential will expire in one day
            os.remove(usercred_file)
            logger.warning('Removed old cert file ' + usercred_file)
            maybe_renew_genicred.timestamp = time.time()


maybe_renew_genicred.timestamp = time.time()


def get_reservable_nodes(ad):
    """get_reservable_nodes

    """
    rspecfile = tempfile.NamedTemporaryFile(delete=False)
    rspecfile.write(ad.text.encode())
    rspecfile.close()
    tree = ET.parse(rspecfile.name)
    os.unlink(rspecfile.name)
    root = tree.getroot()
    # find the element has reservable_types
    e = root.find(".//{http://www.protogeni.net/resources/rspec/ext/emulab/1}reservable_types")
    reservable_type = e[0].attrib['name']

    reservable_nodes = []
    for node in ad.nodes:
        if reservable_type in node.hardware_types:
            reservable_node = Node(component_name=node.name,
                                   component_id=node.component_id,
                                   type=reservable_type,
                                   available=node.available)
            # print(dir(node))
            reservable_nodes.append(reservable_node)
    return reservable_nodes


def parse_manifest(ad):
    """parse_manifest

    """
    rspecfile = tempfile.NamedTemporaryFile(delete=False)
    rspecfile.write(ad.text.encode())
    rspecfile.close()
    tree = ET.parse(rspecfile.name)
    os.unlink(rspecfile.name)
    root = tree.getroot()
    # find the element has reservable_types
    nodes = root.findall(".//{http://www.geni.net/resources/rspec/3}node")

    nodelist = []
    for node in nodes:
        client_id = node.attrib['client_id'] # eg. 'node1'
        # component_id = node.attrib['component_id']
        # sliver_id = node.attrib['sliver_id']

        element_slivertype = node.find(".//{http://www.geni.net/resources/rspec/3}sliver_type")
        slivertype = element_slivertype.attrib['name']

        # element_interface = node.find(".//{http://www.geni.net/resources/rspec/3}interface")
        element_vnode = node.find(".//{http://www.protogeni.net/resources/rspec/ext/emulab/1}vnode")
        element_host = node.find(".//{http://www.geni.net/resources/rspec/3}host")
        element_login = node.find(
            ".//{http://www.geni.net/resources/rspec/3}services//{http://www.geni.net/resources/rspec/3}login")
        newnode = Vnode(name=client_id,                     # 'node1'
                        node=element_vnode.attrib['name'],  # 'pc1' or 'pc2'
                        type=slivertype,                    # 'raw-pc'
                        hardware_type=element_vnode.attrib['hardware_type'],  # 'x3651'
                        disk_image=element_vnode.attrib['disk_image'],
                        hostname=element_login.attrib['hostname'],
                        ipv4=element_host.attrib['ipv4'])
        nodelist.append(newnode)
    return nodelist

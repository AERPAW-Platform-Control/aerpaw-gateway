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


PARSE_PL_FILE = os.getenv('PARSE_PL_FILE')
ADMIN_BOSS = os.getenv('ADMIN_BOSS')
SCP_CMD = 'scp -i {}'.format(os.getenv('SSH_KEY'))
SSH_CMD = 'ssh -i {} {}'.format(os.getenv('SSH_KEY'), ADMIN_BOSS)
usercred_file = '{}/.bssw/geni/emulab-ch2-{}-usercred.xml'.format(str(Path.home()),
                                                                  os.getenv('GENILIB_USER'))


def send_request(emulab_cmd):
    """send_request
        issue emulab cmd to boss machine of emulab

        :param emulab_cmd: string type
        :rtype: emulab stdout, string type
    """
    print(emulab_cmd)
    emulab_cmd_args = shlex.split(emulab_cmd)
    try:
        emulab_stdout = subprocess.check_output(emulab_cmd_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        print(err.output)
        if b'Profile does not exist' in err.output:
            abort(404, description="Profile does not exist")
        elif b'unknown user' in err.output:
            abort(404, description="Unknown user")
        elif b'No such project' in err.output:
            abort(404, description="No such project")
        elif b'No such instance' in err.output:
            abort(404, description="No such instance")
        elif b'Search Failed' in err.output:
            abort(404, description="Search Failed")
        else:
            abort(500, description=err.output.decode("utf-8"))
    print(emulab_stdout)
    return emulab_stdout


def parse_response(emulab_output):
    """parse_response
        Parse emulab perl output to json string

        :param emulab_output: string type
        :rtype: json_string
    """
    print(emulab_output)
    fp = tempfile.NamedTemporaryFile(delete=False)
    fp.write(emulab_output)
    fp.close()
    try:
        json_string = subprocess.check_output([PARSE_PL_FILE, fp.name],
                                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        os.unlink(fp.name)
        print(err.output)
        return err.output

    os.unlink(fp.name)
    print(json_string)
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
    print(script.encode())
    fp_script.close()
    rspec = subprocess.check_output(["python3", fp_script.name])
    print(rspec.decode('utf-8'))
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
    print(xmldata)

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
    print(filepath)
    scp_args = shlex.split('{} {} {}:/tmp/'.format(SCP_CMD, filepath, ADMIN_BOSS))
    # ssh_args = shlex.split('{} chmod 644 /tmp/{}'.format(SSH_CMD, os.path.basename(filepath)))
    try:
        subprocess.check_output(scp_args, stderr=subprocess.STDOUT)
        # subprocess.check_output(ssh_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        print(err.output)
        abort(500, description=err.output.decode("utf-8"))
    return '/tmp/{}'.format(os.path.basename(filepath))


def maybe_renew_genicred():
    if os.path.exists(usercred_file):
        elapsed = time.time() - maybe_renew_genicred.timestamp
        print('last renew time : {}'.format(
            time.asctime(time.localtime(maybe_renew_genicred.timestamp))))
        if elapsed > 24 * 60 * 55:  # the credential will expire in one day
            os.remove(usercred_file)
            print('Removed old cert file ' + usercred_file)
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

import connexion
import six

from swagger_server import util
import os
from flask import abort
import geni.util
import geni.aggregate.cloudlab
import geni.aggregate.pgutil as ProtoGENI


def list_resources(username=None, project=None, experiment=None):  # noqa: E501
    """list resources

    List resources # noqa: E501

    :param username: The username for the request
    :type username: str
    :param project: Project pid
    :type project: str
    :param experiment: if experiment id is given, manifest rspec of the experiment will be returned.
    :type experiment: str

    :rtype: str
    """
    context = geni.util.loadContext(key_passphrase=os.getenv('PASSWORD'))
    print(context.cf.key)
    print(context.cf.cert)
    try:
        if project and experiment:
            urn = 'urn:publicid:IDN+exogeni.net:{}+slice+{}'.format(project, experiment)
            print(urn)
            ad = geni.aggregate.cloudlab.Renci.listresources(context, urn)
        else:
            ad = geni.aggregate.cloudlab.Renci.listresources(context)
    except ProtoGENI.AMError as err:
        abort(400, description=err.text)

        # maybe we want to parse the rspec and check username before return?
    return ad.text


""" use ssh command instead of geni-lib
def list_resources(username=None, project=None, experiment=None):  # noqa: E501

    emulab_cmd = '{} sudo -u {} /usr/testbed/libexec/ptopgen -x -g 2 -r -f'.format(emulab.CMD_PREFIX, emulab.ADMIN)
    emulab_cmd_args = shlex.split(emulab_cmd)
    try:
        emulab_stdout = subprocess.check_output(emulab_cmd_args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        abort(500)

    return emulab_stdout
"""

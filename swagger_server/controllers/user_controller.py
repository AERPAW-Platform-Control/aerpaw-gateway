import connexion
import six

from swagger_server.models.userkey import Userkey  # noqa: E501
from swagger_server import util
from . import emulab
from .resources_controller import list_resources
import json
import logging

logger = logging.getLogger(__name__)


def adduser(body, experiment, project=None):  # noqa: E501
    """add/update user and sshkey on experiment nodes

     # noqa: E501

    :param body: User Object
    :type body: dict | bytes
    :param experiment: experiment for the request
    :type experiment: str
    :param project: project of the experiment
    :type project: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = Userkey.from_dict(connexion.request.get_json())  # noqa: E501
        script = "set -ux; sudo adduser --home /home/newuser/ --disabled-password --gecos '' newuser; \
        sudo usermod -aG root newuser; sudo -u newuser mkdir /home/newuser/.ssh; \
        sudo cp ~/.ssh/* /home/newuser/.ssh/; \
        touch /tmp/authorized_keys; \
        cat ~/.ssh/id_rsa.pub >> /tmp/authorized_keys; \
        echo '{}' >> /tmp/authorized_keys; \
        sudo mv /tmp/authorized_keys /home/newuser/.ssh;\
        sudo chown -R newuser:newuser /home/newuser/.ssh;".format(body.pubkey)
        adduser_script = script.replace('newuser', body.user)

        res = list_resources(experiment=experiment, project=project)
        logger.info(res.vnodes)
        for vnode in res.vnodes:
            if "UBUNTU" in vnode.disk_image:
                emulab_cmd = 'echo "{}" | {} {}@{} -p {} /bin/bash'.format(
                    adduser_script, emulab.SSH_STR, emulab.EMULAB_USER, vnode.hostname, vnode.sshport)
                logger.warning(emulab_cmd)
                emulab_stdout = emulab.send_request(emulab_cmd)
            else:
                logger.error("new os image needs to be supported")
    return 'OK'


import connexion
import six
import json
from . import emulab
from datetime import datetime

from swagger_server.models.api_response import ApiResponse  # noqa: E501
from swagger_server.models.reservation import Reservation  # noqa: E501
from swagger_server import util
import logging

logger = logging.getLogger(__name__)


def create_reservation(body, validate=None):  # noqa: E501
    """create reservation

    Create Reservation # noqa: E501

    :param body: Reservation Object
    :type body: dict | bytes
    :param validate: set to true if just to validate instead of actual reserve
    :type validate: bool

    :rtype: List[ApiResponse]
    """
    if connexion.request.is_json:
        reservation = Reservation.from_dict(connexion.request.get_json())  # noqa: E501
        logger.info(reservation)
    check_option = ''
    if validate:
        check_option = '-n'

    if reservation.username is None:
        reservation.username = emulab.EMULAB_USER

    emulab_cmd = \
        '{} sudo -u {} manage_reservations reserve {} -N /tmp/testreason -t {} -p emulab -s {} -e {} {} {}'.format(
        emulab.SSH_CMD,
        reservation.username,
        check_option,
        reservation.type,
        reservation.start,
        reservation.end,
        reservation.project,
        reservation.nodes)

    emulab_stdout = emulab.send_request(emulab_cmd)
    json_string = emulab.parse_response(emulab_stdout)
    response = ApiResponse(**(json.loads(json_string)))

    return response


def delete_reservation(project, reservation, username=None, cluster=None):  # noqa: E501
    """delete reservation

        Delete Reservation # noqa: E501

        :param project: The project name
        :type project: str
        :param reservation: reservation uuid to delete
        :type reservation: str
        :param username: username who request to delete
        :type username: str
        :param cluster: either cluster name or cluster_urn
        :type cluster: str

        :rtype: List[ApiResponse]
        """
    if username is None:
        username = emulab.EMULAB_USER

    emulab_cmd = '{} sudo -u {} manage_reservations delete {} {}'.format(
        emulab.SSH_CMD, username, project, reservation)

    emulab_stdout = emulab.send_request(emulab_cmd)
    json_string = emulab.parse_response(emulab_stdout)
    response = ApiResponse(**(json.loads(json_string)))
    return response


def get_reservation(username=None, cluster=None):  # noqa: E501
    """get reservation under user

    get reservation under user # noqa: E501

    :param username: username for the request
    :type username: str
    :param cluster: either cluster name or cluster_urn
    :type cluster: str

    :rtype: List[Reservation]
    """
    if username is None:
        username = emulab.EMULAB_USER

    emulab_cmd = '{} sudo -u {} manage_reservations list'.format(emulab.SSH_CMD, username)
    emulab_stdout = emulab.send_request(emulab_cmd)
    json_string = emulab.parse_response(emulab_stdout)

    reservations = []
    if json_string:
        reservations_dict = json.loads(json_string).get('reservations')
        for record in reservations_dict.values():
            startstamp = datetime.fromisoformat(record['start'].replace("Z", "+00:00")).timestamp()
            endstamp = datetime.fromisoformat(record['end'].replace("Z", "+00:00")).timestamp()
            record['start'] = str(int(startstamp))
            record['end'] = str(int(endstamp))
            record['username'] = record.pop('uid')
            record['project'] = record.pop('pid')
            record['experiment'] = record.pop('notes')
            record['cluster'] = record.pop('cluster_id')
            # print(reservation)
            for k in list(record):
                if not getattr(Reservation, k, None):
                    logger.info(k + ":" + str(record[k]) + " is ignored")
                    del record[k]
            reservation = Reservation(**record)
            reservations.append(reservation)

    return reservations




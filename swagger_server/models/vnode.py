# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Vnode(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, name: str=None, type: str=None, disk_image: str=None, hostname: str=None, ipv4: str=None):  # noqa: E501
        """Vnode - a model defined in Swagger

        :param name: The name of this Vnode.  # noqa: E501
        :type name: str
        :param type: The type of this Vnode.  # noqa: E501
        :type type: str
        :param disk_image: The disk_image of this Vnode.  # noqa: E501
        :type disk_image: str
        :param hostname: The hostname of this Vnode.  # noqa: E501
        :type hostname: str
        :param ipv4: The ipv4 of this Vnode.  # noqa: E501
        :type ipv4: str
        """
        self.swagger_types = {
            'name': str,
            'type': str,
            'disk_image': str,
            'hostname': str,
            'ipv4': str
        }

        self.attribute_map = {
            'name': 'name',
            'type': 'type',
            'disk_image': 'disk_image',
            'hostname': 'hostname',
            'ipv4': 'ipv4'
        }
        self._name = name
        self._type = type
        self._disk_image = disk_image
        self._hostname = hostname
        self._ipv4 = ipv4

    @classmethod
    def from_dict(cls, dikt) -> 'Vnode':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Vnode of this Vnode.  # noqa: E501
        :rtype: Vnode
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self) -> str:
        """Gets the name of this Vnode.


        :return: The name of this Vnode.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Vnode.


        :param name: The name of this Vnode.
        :type name: str
        """

        self._name = name

    @property
    def type(self) -> str:
        """Gets the type of this Vnode.


        :return: The type of this Vnode.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Vnode.


        :param type: The type of this Vnode.
        :type type: str
        """

        self._type = type

    @property
    def disk_image(self) -> str:
        """Gets the disk_image of this Vnode.


        :return: The disk_image of this Vnode.
        :rtype: str
        """
        return self._disk_image

    @disk_image.setter
    def disk_image(self, disk_image: str):
        """Sets the disk_image of this Vnode.


        :param disk_image: The disk_image of this Vnode.
        :type disk_image: str
        """

        self._disk_image = disk_image

    @property
    def hostname(self) -> str:
        """Gets the hostname of this Vnode.


        :return: The hostname of this Vnode.
        :rtype: str
        """
        return self._hostname

    @hostname.setter
    def hostname(self, hostname: str):
        """Sets the hostname of this Vnode.


        :param hostname: The hostname of this Vnode.
        :type hostname: str
        """

        self._hostname = hostname

    @property
    def ipv4(self) -> str:
        """Gets the ipv4 of this Vnode.


        :return: The ipv4 of this Vnode.
        :rtype: str
        """
        return self._ipv4

    @ipv4.setter
    def ipv4(self, ipv4: str):
        """Sets the ipv4 of this Vnode.


        :param ipv4: The ipv4 of this Vnode.
        :type ipv4: str
        """

        self._ipv4 = ipv4

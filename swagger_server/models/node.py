# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Node(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, component_name: str=None, component_id: str=None, type: str=None, free: bool=None):  # noqa: E501
        """Node - a model defined in Swagger

        :param component_name: The component_name of this Node.  # noqa: E501
        :type component_name: str
        :param component_id: The component_id of this Node.  # noqa: E501
        :type component_id: str
        :param type: The type of this Node.  # noqa: E501
        :type type: str
        :param free: The free of this Node.  # noqa: E501
        :type free: bool
        """
        self.swagger_types = {
            'component_name': str,
            'component_id': str,
            'type': str,
            'free': bool
        }

        self.attribute_map = {
            'component_name': 'component_name',
            'component_id': 'component_id',
            'type': 'type',
            'free': 'free'
        }
        self._component_name = component_name
        self._component_id = component_id
        self._type = type
        self._free = free

    @classmethod
    def from_dict(cls, dikt) -> 'Node':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Node of this Node.  # noqa: E501
        :rtype: Node
        """
        return util.deserialize_model(dikt, cls)

    @property
    def component_name(self) -> str:
        """Gets the component_name of this Node.


        :return: The component_name of this Node.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name: str):
        """Sets the component_name of this Node.


        :param component_name: The component_name of this Node.
        :type component_name: str
        """

        self._component_name = component_name

    @property
    def component_id(self) -> str:
        """Gets the component_id of this Node.


        :return: The component_id of this Node.
        :rtype: str
        """
        return self._component_id

    @component_id.setter
    def component_id(self, component_id: str):
        """Sets the component_id of this Node.


        :param component_id: The component_id of this Node.
        :type component_id: str
        """

        self._component_id = component_id

    @property
    def type(self) -> str:
        """Gets the type of this Node.


        :return: The type of this Node.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this Node.


        :param type: The type of this Node.
        :type type: str
        """

        self._type = type

    @property
    def free(self) -> bool:
        """Gets the free of this Node.


        :return: The free of this Node.
        :rtype: bool
        """
        return self._free

    @free.setter
    def free(self, free: bool):
        """Sets the free of this Node.


        :param free: The free of this Node.
        :type free: bool
        """

        self._free = free

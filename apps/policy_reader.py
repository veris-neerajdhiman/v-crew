#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.policy_reader
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Read policy source/target pattern and return service readable response
"""

import re


def get_service_names_from_policy_permission_set(policy_list):
    """

    :param policy_list: Policy permission dict
    :return: service names
    """
    service = []
    for permission in policy_list:
        resource = permission.get('target')
        if resource:
            string = resource.split(':')[-2]
            service.append(string)
    return service

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.policy
~~~~~~~~~~~~~~~~~

- This file contains all conversation between Organization & Member Service and AM server
"""

# future
from __future__ import unicode_literals

# 3rd party
import requests

# Django
from django.conf import settings

# local


# own app


ADD_POLICY_URL = '{0}{1}'.format(getattr(settings, 'AM_SERVER_URL'),
                                      getattr(settings, 'ADD_POLICY_API_PATH'))
VALIDATE_POLICY_URL = '{0}{1}'.format(getattr(settings, 'AM_SERVER_URL'),
                                      getattr(settings, 'VALIDATE_POLICY_API_PATH'))
LIST_POLICY_URL = '{0}{1}'.format(getattr(settings, 'AM_SERVER_URL'),
                                      getattr(settings, 'GET_POLICY_API_PATH'))

def add_organization_default_policies(user_uuid, organization_uuid):
    """

    :param user_uuid: user/owner uuid
    :param organization_uuid: organization uuid

    Following permission will be added by default
    Member, VRT, Widget, Process.


    SAMPLE POST Data :
        {
        "source":"user:2db95648-b5ea-458a-9f07-a9ef51bbca21",
        "source_permission_set":[
            {
            "target":"vrn:resource:organization:",
            "create": true,
            "read":true,
            "update":true,
            "delete":true
            }]

    }
    """

    source = 'user:{user_uuid}:{org_identifier}:{org_uuid}:'.format(
        user_uuid=user_uuid,
        org_identifier=getattr(settings, 'ORGANIZATION_IDENTIFIER'),
        org_uuid=organization_uuid
    )

    permission_set = []

    # organization permission set for own object
    org_permissions_set = {
        'target': 'vrn:resource:user:{user_uuid}:{org_identifier}:{org_uuid}:'.format(
            user_uuid=user_uuid,
            org_identifier=getattr(settings, 'ORGANIZATION_IDENTIFIER'),
            org_uuid=organization_uuid)
    }

    org_permissions_set.update(getattr(settings, 'DEFAULT_ORGANIZATION_PERMISSION_SET'))

    # permission set for organization services
    default_services = getattr(settings, 'DEFAULT_ORGANIZATIONS_SERVICES')

    for service in default_services:
        permissions = {
            'target': 'vrn:resource:user:{user_uuid}:{org_identifier}:{org_uuid}:{service}:'.format(
                user_uuid=user_uuid,
                org_identifier=getattr(settings, 'ORGANIZATION_IDENTIFIER'),
                org_uuid=organization_uuid,
                service=service
            )
        }

        permissions.update(getattr(settings, 'DEFAULT_ORGANIZATION_PERMISSION_SET'))
        permission_set.append(permissions)

    permission_set.append(org_permissions_set)

    data = {
        'source': source,
        'source_permission_set': permission_set
    }

    rq = requests.post(ADD_POLICY_URL, json=data, verify=True)

    return rq


def check_user_policy_for_organization(user_uuid, org_uuid, action):
    """
    SAMPLE POST Data :
        {
          "resource": "vrn:resource:organization:",
          "source": "user:2db95648-b5ea-458a-9f07-a9ef51bbca21",
          "action": "read"
        }
    }
    """
    data = {}
    if action == 'create':
        data = {
            'source': 'user:{0}:'.format(user_uuid),
            'resource': 'vrn:resource:organization:',
            'action': 'create'
        }
    elif action in ('read', 'update', 'delete'):
        data = {
            'source': 'user:{0}:organization:{1}:'.format(user_uuid, org_uuid),
            'resource': 'vrn:resource:user:{0}:organization:{1}:'.format(user_uuid, org_uuid),
            'action': action
        }

    rq = requests.post(VALIDATE_POLICY_URL, json=data, verify=True).json()

    return rq.get('allowed')


def get_source_services(user_uuid, org_uuid):
    """

    :return: Source services
    """
    source = 'user:{user_uuid}:{org_identifier}:{org_uuid}:'.format(
        user_uuid=user_uuid,
        org_identifier=getattr(settings, 'ORGANIZATION_IDENTIFIER'),
        org_uuid=org_uuid
    )

    params = {
        'source': source
    }
    rq = requests.get(LIST_POLICY_URL, params=params, verify=True)

    return rq.json()

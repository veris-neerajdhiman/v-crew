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

def add_organization_default_policies(organization_uuid):
    """

    :param organization_uuid: organization uuid

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
    permission_set = []

    # add target in permission set

    # organization permission set for own object
    org_permissions = getattr(settings, 'DEFAULT_ORGANIZATION_PERMISSION_SET')

    # ToDo : not adding user token in resource, only validating with org object

    org_permissions.update({
        'target': 'vrn:resource:{0}:{1}'.format(getattr(settings, 'ORGANIZATION_IDENTIFIER'),
                                                organization_uuid)
    })

    permission_set.append(org_permissions)

    # organization permission set for Member service
    member_permissions = getattr(settings, 'DEFAULT_MEMBER_PERMISSION_SET')

    member_permissions.update({
        'target': 'vrn:resource:{0}:'.format(getattr(settings, 'MEMBER_IDENTIFIER'))
    })

    permission_set.append(member_permissions)

    data = {
        'source': '{0}:{1}'.format(getattr(settings, 'ORGANIZATION_IDENTIFIER'), organization_uuid),
        'source_permission_set':permission_set
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
            'source': 'user:{0}'.format(user_uuid),
            'resource': 'vrn:resource:organization:',
            'action': 'create'
        }
    elif action in ('read', 'update', 'delete'):
        data = {
            'source': 'organization:{0}'.format(org_uuid),
            'resource': 'vrn:resource:organization:{0}'.format(org_uuid),
            'action': 'read'
        }

    rq = requests.post(VALIDATE_POLICY_URL, json=data, verify=True).json()

    return rq.get('allowed')

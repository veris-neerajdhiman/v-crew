#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.signals
~~~~~~~~~~~~~~~~~~

- This file contains the Organization app signals
"""

# future
from __future__ import unicode_literals

# 3rd party
import requests

# Django
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from apps import policy
from apps.members.models import Member

# own app
from apps.organization.models import Organization


@receiver(post_save, sender=Organization)
def add_default_policies_for_organization_on_am_server(sender, instance, created=False, **kwargs):
    """Here default services for Organization will be enabled by adding policies on AM server

    :param sender: Signal sender
    :param instance: Organization instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    if created:
        # Add Policy for Organization
        policy.add_organization_default_policies(instance.owner, instance.token)


# @receiver(post_save, sender=Organization)

def add_organization_owner_as_orgnization_member(sender, instance, created=False, **kwargs):
    """Here Organization owner will be added as Organization member too , so That we can assign him default RunTimes

    :param sender: Signal sender
    :param instance: Organization instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    # ToDo : Must be handled by System Workflow, this is a Temporary solution

    if created:

        # get user details
        user_get_api = 'micro-service/user/{user_uuid}/'.format(user_uuid=instance.owner)
        user_server_url = getattr(settings, 'USER_SERVER_URL', None)

        url = '{0}{1}'.format(user_server_url, user_get_api)

        response = requests.get(url).json()

        data = {
            'name': response.get('name') if response.get('name') is not None else '',
            'email': response.get('email'),
            'organization': instance,
            'user': instance.owner,
            'type': 'user',
        }

        # add as Member
        Member.objects.create(**data)

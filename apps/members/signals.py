#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.signals
~~~~~~~~~~~~~~~~~~

- This file contains the Member app signals
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.db.models.signals import post_save
from django.dispatch import receiver

# local
from apps import policy

# own app
from apps.members.models import Member


@receiver(post_save, sender=Member)
def add_default_policies_for_organization_on_am_server(sender, instance, created=False, **kwargs):
    """Here default services for Member will be enabled by adding policies on AM server

    :param sender: Signal sender
    :param instance: Member instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    if created:
        # Add Policy for Member
        policy.add_member_default_policies(instance.organization.owner, instance.organization.token, instance.uuid)

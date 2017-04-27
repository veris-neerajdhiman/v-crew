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

# Django
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

# local
from apps import policy

# own app
from apps.organization.models import Organization


@receiver(post_save, sender=Organization)
def add_default_policies_for_organization_on_am_server(sender, instance, created=False, **kwargs):
    """Here default services for Organization will be enabled by adding policies on AM server

    :param sender: Signal sender
    :param instance: User instance
    :param created: If new obj is created or updated
    :param kwargs: Signal kwargs
    """
    if created:
        # Add Policy for Organization
        policy.add_organization_default_policies(instance.owner, instance.token)

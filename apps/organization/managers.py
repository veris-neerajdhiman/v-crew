#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.managers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Includes Models Managers
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.db import models

# local

# own app


class UserOrganizationManager(models.Manager):
    """

    """
    def get_member_organization_queryset(self, username):
        return super(UserOrganizationManager, self).get_queryset().filter(
            organization_members__user=username)

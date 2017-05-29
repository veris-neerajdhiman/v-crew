#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.models
~~~~~~~~~~~~~~~~~~~~~

- This file contains the Members models that will map into DB tables.
"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _


# local
from apps.organization.models import Organization

# own app
from apps.members import config


class Member(models.Model):
    """

    """
    # attributes
    uuid = models.UUIDField(
        _('Member Unique Identifier'),
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text=_('Member uuid, this token will uniquely identify Member.'),
    )
    name = models.CharField(
        _('Member Name'),
        null=False,
        blank=False,
        max_length=64,
        help_text=_('Required. 64 characters or fewer.')
    )
    email = models.EmailField(
        _('Member Email.'),
        help_text=_('Primary Contact of Member, immutable.')
    )
    organization = models.ForeignKey(Organization,
                                     related_name='organization_members',
                                     to_field='token',
                                     on_delete=models.CASCADE,
                                     help_text=_('Member Organization.')
    )
    user = models.UUIDField(
        _('Member associated User UUID'),
        null=False,
        blank=False,
        help_text=_('User uuid, this uid will identify associated User with respective Member.'),
    )
    type = models.CharField(
        _('Member type.'),
        max_length=config.MAXLENGTH,
        choices=config.MEMBER_TYPES,
        help_text=_('Member type, for internal user only'),
    )
    created_at = models.DateTimeField(
        _('Organization Creation time.'),
        auto_now_add=True,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        _('Organization Modification time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("Organization Member")
        verbose_name_plural = _("Organization Members")
        unique_together = ('email', 'organization', )
        ordering = ["-id"]

    # Functions
    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

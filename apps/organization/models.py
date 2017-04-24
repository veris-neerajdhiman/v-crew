#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.models
~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains organization micro-service models.
  Organizations can be created by the ``authenticated`` & ``verified`` users.

"""

# future
from __future__ import unicode_literals

# 3rd party
import uuid
from imagekit.models import ImageSpecField
from pilkit.processors.resize import ResizeToFill

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from apps.utils import media_folder

# own app


class Organization(models.Model):
    """
    """
    token = models.UUIDField(
        _('Organization Unique Identifier'),
        default=uuid.uuid4,
        unique=True,
        editable=False,
        help_text=_('Organization uuid, this token will uniquely identify Organization.'),
    )
    # attributes
    name = models.CharField(
        _('Organization Name'),
        null=False,
        blank=False,
        max_length=64,
        help_text=_('Required. 64 characters or fewer.')
    )
    avatar = models.ImageField(
        _('Organization Logo'),
        upload_to=media_folder
    )
    avatar_thumbnail = ImageSpecField(
        source='avatar',
        processors=[ResizeToFill(100, 50)],
        format='JPEG',
        options={'quality': 60}
    )
    owner = models.UUIDField(
        _('Owner Unique Identifier'),
        help_text=_('User uuid, this token will identify who is the owner of respective Organization.'),
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
        verbose_name = _("Organization")
        verbose_name_plural = _("Organization")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

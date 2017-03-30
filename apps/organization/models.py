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
from imagekit.models.fields import ProcessedImageField
from pilkit.processors.resize import ResizeToFit

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local
from apps.utils import media_folder

# own app


class Organization(models.Model):
    """
    """

    # attributes
    name = models.CharField(
        _('Organization Name'),
        null=False,
        blank=False,
        max_length=64,
        help_text=_('Required. 64 characters or fewer.')
    )
    logo = ProcessedImageField(
        upload_to=media_folder,
        null=False,
        blank=False,
        processors=[ResizeToFit(1024, 1024, upscale=False)]
    )
    created_at = models.DateTimeField(
        _('Organization Creation time.'),
        auto_now=False,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        _('Organization Modification time.'),
        auto_now=False,
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

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-  apps.organization.admin
~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains admin models of Organization micro service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib import admin

# local

# own app
from apps.organization import models


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'token', 'name', 'avatar', 'user', 'created_at', 'modified_at', )
    list_display_links = ('id', 'name', )
    search_fields = ('name', )
    list_per_page = 20
    ordering = ('-id', )

    def avatar_thumbnail(self, obj):
        """

        :param obj: Organization instance
        :return: user avatar thumbanil
        """
        return '<img width="36" height="36" src="%s"/>' % obj.avatar if bool(obj.avatar) else ''

        avatar.allow_tags = True

admin.site.register(models.Organization, OrganizationAdmin)

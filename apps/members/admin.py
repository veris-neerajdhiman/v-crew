#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
-  apps.members.admin
~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains admin models of Members micro service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib import admin

# local

# own app
from apps.members import models


class MemberAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('id', 'name', 'uuid', 'email', 'organization', 'user', 'type', )
    list_display_links = ('id', 'name', 'email', )
    list_filter = ('type', )
    search_fields = ('name', 'email', 'uuid', 'organization__name', 'organization__token', 'user')
    raw_id_fields = ['organization', ]
    ordering = ('-id', )
    list_per_page = 20

admin.site.register(models.Member, MemberAdmin)

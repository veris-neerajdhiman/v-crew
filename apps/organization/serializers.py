#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains organization micro-service models.
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import serializers

# Django

# local
from apps.members.models import Member

# own app
from apps.organization import models


class OrganizationSerializer(serializers.ModelSerializer):
    """

    """
    uuid = serializers.CharField(source='token', read_only=True)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Organization
        exclude = ('id', 'token', 'created_at', 'modified_at',)

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains organization micro-service serializers.
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import serializers
from datetime import datetime

# Django

# local

# own app
from apps.organization import models


class OrganizationSerializer(serializers.ModelSerializer):
    """

    """
    id = serializers.ReadOnlyField()

    class Meta:
        model = models.Organization
        exclude = ('created_at', 'modified_at',)

    def create(self, validated_data):
        """

        :param validated_data: Validated data
        :return: Organization instance
        """
        created_at = modified_at = datetime.now()

        validated_data.update({
            'created_at': created_at,
            'modified_at': modified_at
        })

        return super(OrganizationSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """

        :param instance: Organization instance to be updated
        :param validated_data: Validated data
        :return: Organization instance
        """
        modified_at = datetime.now()

        validated_data.update({
            'modified_at': modified_at
        })

        return super(OrganizationSerializer, self).update(instance, validated_data)

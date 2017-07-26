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
from django.conf import settings

# local

# own app
from apps.organization import models


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    """


    """
    url = serializers.SerializerMethodField()
    uuid = serializers.CharField(source='token',
                                 read_only=True)
    avatar = serializers.URLField(required=False)

    # avatar = serializers.ImageField(required=False)
    # avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Organization
        exclude = ('token', 'user', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrganizationSerializer, self).__init__(*args, **kwargs)

    def get_url(self, obj):
        """

        :param obj: Organization object
        :return: absolute url of Organization
        """
        from django.urls import reverse
        request = self.context.get('request')

        url_name = '{app_namespace}:organization-urls:organization-detail'.\
            format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        return request.build_absolute_uri(
            reverse(url_name, args=(str(obj.token), ))
        )

    def create(self, validated_data):
        """

        :param validated_data: Validated data
        :return: Organization obj
        """
        user = self.context.get('request').user

        validated_data.update({
            'user': user
        })

        return models.Organization.objects.create(**validated_data)
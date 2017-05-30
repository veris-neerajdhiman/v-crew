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
    avatar = serializers.ImageField(required=False)
    avatar_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = models.Organization
        exclude = ('token', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrganizationSerializer, self).__init__(*args, **kwargs)

    def get_url(self, obj):
        """

        :param obj:
        :return: absolute url of Organization
        """
        from django.urls import reverse

        url_name = '{app_namespace}:organization-urls:organization-detail'.format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        owner = self.request.parser_context.get('kwargs').get('owner')

        return self.request.build_absolute_uri(reverse(url_name,
                                                       args=(owner, str(obj.token), )
                                                       ))

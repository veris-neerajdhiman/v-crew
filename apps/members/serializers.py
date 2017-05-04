#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.member.serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains member micro-service models.
"""

# future
from __future__ import unicode_literals

# 3rd party
import requests
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import NotAcceptable

# Django
from django.conf import settings

# local
from apps.organization.serializers import OrganizationSerializer

# own app
from apps.members import models, config


class MemberSerializer(serializers.ModelSerializer):
    """This Serializer is used when we qil retrieve, update a Member.

    """
    url = serializers.SerializerMethodField()

    class Meta:
        model = models.Member
        fields = ('url', 'uuid', 'name', 'email', 'user', 'type', 'organization')
        read_only_fields = ('id', 'email', )


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberSerializer, self).__init__(*args, **kwargs)

    def get_url(self, obj):
        """

        :param obj:
        :return:
        """
        from django.urls import reverse

        # import ipdb;ipdb.set_trace()
        url_name = '{app_namespace}:member-urls:members-detail'.format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        owner = self.request.parser_context.get('kwargs').get('owner')
        organization = self.request.parser_context.get('kwargs').get('organization')

        return self.request.build_absolute_uri(reverse(url_name,
                                                       args=(owner, organization, obj.uuid)))


class MemberAddSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are adding a Member.

    """
    url = serializers.SerializerMethodField()
    email = serializers.EmailField(required=False,)
    uuid = serializers.UUIDField(read_only=True)
    user = serializers.UUIDField(required=False)  # to be added later when we willa dd shadow user
    type = serializers.ChoiceField(required=True,
                                   choices=config.MEMBER_TYPES)

    class Meta:
        model = models.Member
        exclude = ('id', 'created_at', 'modified_at', )
        validators = [
           UniqueTogetherValidator(
                queryset=models.Member.objects.all(),
                fields=('email', 'organization', )
           )
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberAddSerializer, self).__init__(*args, **kwargs)

    def get_url(self, obj):
        """

        :param obj:
        :return:
        """
        from django.urls import reverse

        # import ipdb;ipdb.set_trace()
        url_name = '{app_namespace}:member-urls:members-detail'.format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        owner = self.request.parser_context.get('kwargs').get('owner')
        organization = self.request.parser_context.get('kwargs').get('organization')

        return self.request.build_absolute_uri(reverse(url_name,
                                                       args=(owner, organization, obj.uuid)))

    def _get_user_api(self):
        """

        """
        if config.USER_SERVER_URL.endswith('/') and config.USER_CREATE_API.startswith('/'):
            return '{0}{1}'.format(config.USER_SERVER_URL[:-1], config.USER_CREATE_API)
        elif not config.USER_SERVER_URL.endswith('/') and not config.USER_CREATE_API.startswith('/'):
            return '{0}/{1}'.format(config.USER_SERVER_URL, config.USER_CREATE_API)
        return '{0}{1}'.format(config.USER_SERVER_URL, config.USER_CREATE_API)

    def _get_default_image(self):
        """
        """
        return config.DEFAULT_IMAGE_PATH

    def _get_or_create_shadow_user(self, email):
        """
            - Here we manage creation of Shadow User in Authentication Server.
            - First we will check wether user with same email if not only then we will create shadow user.
        """
        url = self._get_user_api()
        image = open(self._get_default_image(), 'rb')

        # ToDo : Not checking for any error in below API
        return requests.post(url, files={'avatar': image}, data={'email': email}).json()

    def create(self, validated_data):
        """

        :param validated_data: Validated data.
        """
        # check User Server Url has been set mentioned or not
        if config.USER_SERVER_URL is None:
            raise NotAcceptable('you have not mentioned User Server Url in settings.')

        # create shadow user and save user token in Member instance
        email = validated_data.get('email')
        user = self._get_or_create_shadow_user(email)

        validated_data.update({
            'user': user.get('uuid')
        })

        return super(MemberAddSerializer, self).create(validated_data)


class MemberShipSerializer(serializers.ModelSerializer):
    """

    """
    organization = OrganizationSerializer()

    class Meta:
        model = models.Member
        fields = ('uuid', 'name', 'user', 'organization')

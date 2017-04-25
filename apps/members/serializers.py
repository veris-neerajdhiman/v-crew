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

# local

# own app
from apps.members import models, config


class MemberSerializer(serializers.ModelSerializer):
    """This Serializer is used when we qil retrieve, update a Member.

    """
    class Meta:
        model = models.Member
        exclude = ('created_at', 'modified_at', )
        read_only_fields = ('id', 'email', )


class MemberAddSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are adding a Member.

    """
    email = serializers.EmailField(required=False,)
    user = serializers.UUIDField(required=False)  # to be added later when we willa dd shadow user
    type = serializers.ChoiceField(required=True,
                                   choices=config.MEMBER_TYPES)

    class Meta:
        model = models.Member
        exclude = ('created_at', 'modified_at', )
        validators = [
           UniqueTogetherValidator(
                queryset=models.Member.objects.all(),
                fields=('email', 'organization', )
           )
        ]

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

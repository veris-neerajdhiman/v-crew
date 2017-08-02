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
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.exceptions import NotAcceptable

# Django
from django.conf import settings

# local
from apps.organization.serializers import OrganizationSerializer
from auth import jwt

# own app
from apps.members import models, config


class MemberSerializer(serializers.ModelSerializer):
    """This Serializer is used when we qil retrieve, update a Member.

    """
    url = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()

    class Meta:
        model = models.Member
        fields = ('url', 'uuid', 'name', 'email', 'user', 'type', 'organization', 'created_at', 'modified_at', 'token', )
        read_only_fields = ('id', 'email', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberSerializer, self).__init__(*args, **kwargs)

    def _get_jwt_payload(member):
        """
        :param user: Member object
        :return: jwt necessary information
        """
        expiration_time = datetime.utcnow() + timedelta(seconds=getattr(settings, 'TOKEN_EXPIRATION_TIME', 432000))

        return {
            'info': {
                'name': member.name,
                'email': member.email,
                'type': member.type,
                'uuid': member.uuid
            },
            'exp': expiration_time,
            'iat': datetime.utcnow(),
            'iss': getattr(settings, 'ISSUER', 'noapp'),
            'aud': getattr(settings, 'AUDIENCE', 'noapp-services')
        }

    def get_url(self, obj):
        """

        :param obj:
        :return:
        """
        from django.urls import reverse

        url_name = '{app_namespace}:member-urls:members-detail'.format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        owner = self.request.parser_context.get('kwargs').get('owner')
        organization = self.request.parser_context.get('kwargs').get('organization')

        return self.request.build_absolute_uri(reverse(url_name,
                                                       args=(organization, obj.uuid)))

    def get_token(self, obj):
        """

        :param obj: Member object
        :return: Member token
        """

        payload = self._get_jwt_payload(obj)
        return jwt.create_jwt(payload,
                              getattr(settings, 'JWT_PUBLIC_KEY', None),
                              getattr(settings, 'ALGORITHM', 'HS256')
                              )


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
        exclude = ('id', )
        validators = [
           UniqueTogetherValidator(
                queryset=models.Member.objects.all(),
                fields=('email', 'organization', )
           )
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberAddSerializer, self).__init__(*args, **kwargs)

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
        # image = open(self._get_default_image(), 'rb')
        data = {
            'email': email,
            'is_active': False
        }

        user = requests.post(url, data=data).json()

        # ToDo : Not checking for any error in below API
        # return requests.post(url, files={'avatar': image}, data=data).json()
        return user

    def get_url(self, obj):
        """

        :param obj: Member object
        :return: Member-detail API url
        """
        from django.urls import reverse

        url_name = '{app_namespace}:member-urls:members-detail'.format(app_namespace=getattr(settings, 'APP_NAMESPACE'))

        organization = self.request.parser_context.get('kwargs').get('organization')

        return self.request.build_absolute_uri(reverse(url_name,
                                                       args=(organization, obj.uuid)))

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
        username = user.get('email')

        validated_data.update({
            'user': username.replace('@', '__')
        })
        return super(MemberAddSerializer, self).create(validated_data)


class MemberShipSerializer(serializers.ModelSerializer):
    """

    """
    organization = serializers.SerializerMethodField()

    class Meta:
        model = models.Member
        fields = ('uuid', 'name', 'user', 'organization', 'created_at', 'modified_at', )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MemberShipSerializer, self).__init__(*args, **kwargs)

    def get_organization(self, obj):
        """

        :param obj: member Object
        :return: organization data
        """
        return OrganizationSerializer(obj.organization, request=self.request).data

#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
- auth.jwt
~~~~~~~~~~

- This file contains Custom Backend Class to Authenticate User.
"""


# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import authentication
from rest_framework import exceptions

# Django
from django.contrib.auth.models import User
from django.conf import settings

# local
from auth.jwt import validate_jwt


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return None

        valid_token = self._decode_jwt(token)

        username = valid_token.get('user_info').get('email')

        if not username:
            return None

        clean_username = username.replace('@', '__')

        user, created = User.objects.get_or_create(username=clean_username)

        # check user scope for Template-service
        self._check_user_scope(valid_token.get('user_info'))

        return (user, None)

    def _decode_jwt(self, token):
        """
        """
        try:
            return validate_jwt(token,
                                secret=getattr(settings, 'JWT_PUBLIC_KEY', None),
                                aud=getattr(settings, 'AUDIENCE', 'noapp-services'),
                                verify=True)
        except Exception as e:
            raise exceptions.AuthenticationFailed(e)

    def _check_user_scope(self, user_info):
        """

        """
        user_scope = getattr(settings, 'CREW_SCOPE', 'organization')
        if user_scope not in user_info.get('scope'):
            raise exceptions.AuthenticationFailed("User don't have enough permission to access this micro-service")

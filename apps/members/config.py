#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.config
~~~~~~~~~~~~~~

- This file holds the general settings of Member micro-services.
 """

# django
from django.conf import settings

MAXLENGTH = 8
TERMINAL = 'terminal'
USER = 'user'

MEMBER_TYPES = (
    (TERMINAL, TERMINAL),
    (USER, USER),
)

DEFAULT_IMAGE_NAME = 'images/placeholder.png'
DEFAULT_IMAGE_PATH = '{0}/{1}'.format(settings.STATIC_ROOT, DEFAULT_IMAGE_NAME)
USER_CREATE_API = '/micro-service/user/shadow/'
USER_SERVER_URL = getattr(settings, 'USER_SERVER_URL', None)

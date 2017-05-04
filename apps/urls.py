#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.urls
~~~~~~~~~~~~~~

- this file contains all apps urls
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.conf.urls import include, url


# local
from apps.organization import routers as org_router
from apps.members import routers as member_router

# own app


urlpatterns = [
    url(r'', include(org_router, namespace='organization-urls')),
    url(r'', include(member_router, namespace='member-urls')),
]

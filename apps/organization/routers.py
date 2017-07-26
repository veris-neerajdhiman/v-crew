#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.router
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Routers of Organization micro-service
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.conf.urls import url

# own app
from apps.organization import views


UUID_REGEX = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

organization_list = views.OrganizationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

organization_detail = views.OrganizationViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^organization/$',
        organization_list,
        name='organization-list'),
    url(r'^organization/(?P<token>{uuid})/$'.format(uuid=UUID_REGEX),
        organization_detail,
        name='organization-detail'),
]

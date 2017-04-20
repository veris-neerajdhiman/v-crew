#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.router
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Routers of Member micro-service
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.conf.urls import url

# own app
from apps.members import views


UUID_REGEX = '[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}'

members_list = views.MemberViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
members_detail = views.MemberViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    url(r'^user/(?P<owner>{uuid})/organization/(?P<organization>\d+)/member/$'.format(uuid=UUID_REGEX),
        members_list,
        name='members-list'),
    url(r'^user/(?P<owner>{uuid})/organization/(?P<organization>\d+)/member/(?P<pk>\d+)/$'.format(uuid=UUID_REGEX),
        members_detail,
        name='members-detail'),
]

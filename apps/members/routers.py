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

member_organization_list = views.MemberShipViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
    url(r'^user/(?P<owner>{uuid})/organization/(?P<organization>{uuid})/member/$'.format(uuid=UUID_REGEX),
        members_list,
        name='members-list'),
    url(r'^user/(?P<owner>{uuid})/organization/(?P<organization>{uuid})/member/(?P<uuid>{uuid})/$'.format(uuid=UUID_REGEX),
        members_detail,
        name='members-detail'),
    url(r'^member/(?P<member_user_uuid>{uuid})/organization/$'.format(uuid=UUID_REGEX),
        member_organization_list,
        name='members-organizations'),
]

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.views
~~~~~~~~~~~~~~~~~~~~

- This file contains Members micro-service views, every HTTP request/router points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party
import copy
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# Django

# local
from apps import mixins

# own app
from apps import permissions as custom_permissions
from apps.members import models, serializers


class MemberViewSet(mixins.MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """

    """
    model = models.Member
    queryset = model.objects.all()
    serializer_class = serializers.MemberSerializer
    permission_classes = (permissions.IsAuthenticated, custom_permissions.IsUserOrganizationOwner)
    lookup_field = 'uuid'
    lookup_fields = ('uuid', 'organization', )  # to be used in filter

    def get_serializer_class(self):
        """For POST method we will use different Serializer

        :return: Serializer Class
        """
        if self.request:
            if self.request.method == 'POST':
                return serializers.MemberAddSerializer
        return self.serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.update({
            'request': self.request,
        })
        return serializer_class(*args, **kwargs)


    def create(self, request, organization):
        """

        :param request: Django request
        :param organization: organization token.
        :return: Just created Organization
        """

        post_data = copy.deepcopy(request.data)

        # ToDo: Right Now we are using organization directly but later on we have validate this organization Permissions
        # ToDo: only then we will add this organization pk in FK
        post_data.update({
            'organization': organization
        })
        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MemberShipViewSet(viewsets.ModelViewSet):
    """This viewset will be used to list user memberships.

    """
    model = models.Member
    queryset = model.objects.all()
    serializer_class = serializers.MemberShipSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        """

        """
        queryset = super(MemberShipViewSet, self).get_queryset()
        return queryset.filter(user=self.kwargs.get('member_user_uuid'))

    def get_serializer(self, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs.update({
            'request': self.request,
        })
        return serializer_class(*args, **kwargs)
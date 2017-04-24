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
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Django

# local
from apps import mixins, permissions as custom_permissions

# own app
from apps.members import models, serializers


class MemberViewSet(mixins.MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """

    """
    model = models.Member
    queryset = model.objects.all()
    serializer_class = serializers.MemberSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, custom_permissions.IsUserOrganizationOwner)

    lookup_fields = ('pk', 'organization', )  # to be used in filter

    def get_serializer_class(self):
        """For POST method we will use different Serializer

        :return: Serializer Class
        """
        if self.request.method == 'POST':
            return serializers.MemberAddSerializer
        return self.serializer_class

    def create(self, request, owner, organization):
        """

        :param request: Django request
        :param owner: owner/user uuid
        :param organization: organization token.
        :return: Just created Organization
        """

        post_data = request.data

        # ToDo: Right Now we are using organization directly but later on we have validate this organization Permissions
        # ToDo: only then we will add this organization pk in FK
        post_data.update({
            'organization': organization
        })

        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
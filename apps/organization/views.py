#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.views
~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains organization micro-service views, every HTTP request/router points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party
import copy
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# Django

# local
from apps import mixins, utils

# own app
from apps.organization import models, serializers


class OrganizationViewSet(mixins.MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """Organization Viewset

    """
    model = models.Organization
    queryset = model.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated, )
    lookup_field = 'token'
    lookup_fields = ('token', )  # to be used in filter

    def get_serializer_context(self):
        """
         Extra context provided to the serializer class.
        """
        return {
            'request': self.request,  # request object is passed here
            }

    def get_queryset(self, *args, **kwargs):
        """
        """
        queryset = super(OrganizationViewSet, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(user=self.request.user)

        return queryset

    def list(self, request):
        """

        :param request: Django request
        :param owner: owner/user uuid
        :return: User Organization List (Both in which he is member and owner)
        """

        # Here we have to list All organization in which a user is either owner or member
        # We already have qs(1) of Organizations in which User is owner.
        # for Organization in which user is member we can match `owner` uuid in `user` field of Member model and can
        # get Organization list qs()2 and then merge two qs(1) & qs(2) to get entire list of Organizations.

        owner_organization_qs = self.get_queryset()
        member_organization_qs = models.UserOrganization.objects.\
            get_member_organization_queryset(username=request.user.username)

        response = {
            'as_owner': self.get_serializer(owner_organization_qs, many=True).data,
            'as_member': self.get_serializer(member_organization_qs, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)

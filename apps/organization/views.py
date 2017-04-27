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
from rest_framework import viewsets, status
from rest_framework.response import Response

# Django

# local
from apps import mixins, permissions, policy, policy_reader, utils

# own app
from apps.organization import models, serializers


class OrganizationViewSet(mixins.MultipleFieldLookupMixin, viewsets.ModelViewSet):
    """Organization Viewset

    """
    model = models.Organization
    queryset = model.objects.all()
    serializer_class = serializers.OrganizationSerializer
    permission_classes = (permissions.ValidateOrgnizationPermission,)
    lookup_field = 'token'
    lookup_fields = ('token', 'owner', )  # to be used in filter

    def create(self, request, owner):
        """

        :param request: Django request
        :param owner: owner/user uuid
        :return: Just created Organization
        """

        post_data = request.data

        # ToDo: Right Now we are using owner uuid directly but later on we have validate this user Permissions
        # ToDo: only then we will add this uuid in owner
        post_data.update({
            'owner': owner
        })

        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def organization_uuid_list(self, request):
        """

        :return: organization uuid list
        """
        # ToDo: Restrict this API for internal Use Only

        # filter for uuid sent in query_param if any
        filtered_uuids = []
        uuids = self.request.query_params.get('uuids', [])
        if uuids:
            filtered_uuids = self.queryset.exclude(token__in=eval(uuids)).values_list('token', flat=True)
        return Response({'organization_uuids': filtered_uuids}, status=status.HTTP_200_OK)

    def get_organization_service(self, request, owner, token):
        """

        :param request: Django request
        :param owner: owner/user uuid
        :param token: organization uuid
        :return: Organization services
        """
        permission_set = policy.get_source_services(owner, token)

        services = policy_reader.get_service_names_from_policy_permission_set(permission_set.get('source_permission_set'))

        response = utils.get_permissions_from_names(services)

        return Response(response, status=status.HTTP_200_OK)

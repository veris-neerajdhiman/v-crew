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

        post_data = copy.deepcopy(request.data)

        # ToDo: Right Now we are using owner uuid directly but later on we have validate this user Permissions
        # ToDo: only then we will add this uuid in owner
        post_data.update({
            'owner': owner
        })

        serializer = self.get_serializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, owner):
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
        member_organization_qs = models.UserOrganization.objects.get_member_organization_queryset(user_uuid=owner)

        response = {
            'as_owner': self.get_serializer(owner_organization_qs, many=True).data,
            'as_member': self.get_serializer(member_organization_qs, many=True).data
        }

        return Response(response, status=status.HTTP_200_OK)

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

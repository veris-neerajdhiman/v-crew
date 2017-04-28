#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.permissions
~~~~~~~~~~~~~~

- This file holds the general permissions of Organization-Member micro-services.
 """

# drf
from rest_framework import permissions, exceptions, status

# local
from apps import policy
from apps.organization.models import Organization


class CustomForbidden(exceptions.APIException):
    """

    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not authorized to perform this action."


class ValidateOrgnizationPermission(permissions.BasePermission):
    """

    """

    def has_permission(self, request, view):
        """

        """
        action = None
        if request.method == 'POST':
            action = 'create'
        elif request.method in ('GET', 'PATCH', 'DELETE'):
            action = 'read'
        user_uuid = request.parser_context.get('kwargs').get('owner')
        org_uuid = request.parser_context.get('kwargs').get('token')

        if not policy.check_user_policy_for_organization(user_uuid, org_uuid, action):
            raise CustomForbidden
        return True


class ValidateMemberPermission(permissions.BasePermission):
    """

    """

    def has_permission(self, request, view):
        """

        """
        action = None
        if request.method == 'POST':
            action = 'create'
        elif request.method in ('GET', 'PATCH', 'DELETE'):
            action = 'read'
        user_uuid = request.parser_context.get('kwargs').get('owner')

        # exceptional case when member is trying to access his memberships but as user (logged in  from app)
        if user_uuid is None:
            user_uuid = request.parser_context.get('kwargs').get('member_user_uuid')
        org_uuid = request.parser_context.get('kwargs').get('organization')
        member_uuid = request.parser_context.get('kwargs').get('uuid')

        if not policy.check_user_policy_for_member(user_uuid, org_uuid, member_uuid, action):
            raise CustomForbidden
        return True


class IsUserOrganizationOwner(permissions.BasePermission):
    """Here we will verify user UUID used in url w.r.t Organization in url is actually UUID of that Organization
    Owner UUId

    """

    def has_permission(self, request, view):
        """

        """
        filters = {
            'owner': request.parser_context['kwargs'].get('owner'),
            'token': request.parser_context['kwargs'].get('organization')
        }
        if not Organization.objects.filter(**filters):
            raise CustomForbidden
        return True

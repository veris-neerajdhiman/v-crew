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
from apps.organization.models import Organization


class CustomForbidden(exceptions.APIException):
    """

    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not authorized to perform this action."


class IsUserOrganizationOwner(permissions.BasePermission):
    """Here we will verify user UUID used in url w.r.t Organization in url is actually UUID of that Organization
    Owner UUId

    """
    message = "Only gatekeeper has permission to perform this action."

    def has_permission(self, request, view):
        """

        """
        filters = {
            'owner': request.parser_context['kwargs'].get('owner'),
            'pk': request.parser_context['kwargs'].get('organization')
        }
        if not Organization.objects.filter(**filters):
            raise CustomForbidden
        return True

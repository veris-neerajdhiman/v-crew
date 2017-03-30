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
from rest_framework import viewsets, permissions

# Django

# local

# own app
from apps.organization import models, serializers


class OrganizationViewSet(viewsets.ModelViewSet):
    """Organization Viewset

    """
    model = models.Organization
    queryset = model.objects.all()
    serializer_class = serializers.OrganizationSerializer
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny,)


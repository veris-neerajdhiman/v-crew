#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.router
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Routers of Organization micro-service
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import routers

# Django
from django.conf.urls import url

# own app
from apps.organization import views


router = routers.SimpleRouter()
router.register('organization', views.OrganizationViewSet)


urlpatterns = [

]

urlpatterns += router.urls

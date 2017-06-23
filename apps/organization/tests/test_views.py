#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.organization.tests.test_views
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file includes Test cases for Views .

"""

# future
from __future__ import unicode_literals

# 3rd party
import tempfile
from PIL import Image

# Django
from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from urllib.parse import urlencode


class OrganizationTestCase(TestCase):
    """Handles Organization Views Test Cases

    """
    pass

    # ToDo: Move AM & signals to Platform Workflow and then add Test Cases here.
    # def setUp(self):
    #     """
    #
    #     """
    #     self.user_token = 'b0b66cee-1375-43f7-a75e-01d229336f13'



    # def test_org_create(self):
    #     """Test Create Organization Object
    #
    #     """
    #     FixMe: This test case is commented because it need to add org owner as meber and then user on `User`
    #     FixMe: (contd.)  micro-service , So Test env cannot do that. We cannot add Unit test cases un-till
    #     FixMe: (contd.)  Signals and AM policies add/validate moved to platform Workflow.

    #     url = reverse('apps:organization-urls:organization-list', args=(self.user_token, ))
    #     data = {
    #         'name': 'test-organization',
    #     }
    #     response = self.client.post(url, data=data)
    #
    #     self.assertEqual(response.status_code, 201)

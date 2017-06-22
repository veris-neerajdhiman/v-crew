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
    def setUp(self):
        """

        """
        self.user_token = 'b0b66cee-1375-43f7-a75e-01d229336f13'

    def test_org_create(self):
        """Test Create Organization Object

        """
        url = reverse('apps:organization-urls:organization-list', args=(self.user_token, ))
        data = {
            'name': 'test-organization',
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)
    #
    # def test_user_detail(self):
    #     """Test User Object details
    #
    #     """
    #     url = reverse('accounts:user-detail', args=(self.user.uuid, ))
    #     response = self.client.get(url)
    #
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_user_update(self):
    #     """Test Update User Object
    #
    #     """
    #     url = reverse('accounts:user-detail', args=(self.user.uuid, ))
    #     data = urlencode({
    #         'name': 'updated-test'
    #     })
    #     response = self.client.patch(url, content_type="application/x-www-form-urlencoded", data=data)
    #
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_user_delete(self):
    #     """Test Delete Update User Object
    #
    #     """
    #     url = reverse('accounts:user-detail', args=(self.user.uuid, ))
    #
    #     response = self.client.delete(url)
    #
    #     self.assertEqual(response.status_code, 204)
    #
    # def test_shadow_user(self):
    #     """Test Shadow User Create
    #
    #     """
    #     url = reverse('accounts:get-or-create-shadow-user')
    #     data = {
    #         'email': 'test-m4@example.com',
    #         'avatar': self.image,
    #         'password': 123,
    #         'is_active': False
    #     }
    #     response = self.client.post(url, data=data)
    #
    #     self.assertEqual(response.status_code, 201)
    #
    # def test_user_email_unique(self):
    #     """Test User with same email doesn't get created.
    #
    #     """
    #     url = reverse('accounts:user-create')
    #     data = {
    #         'email': 'test@example.com',
    #         'avatar': self.image,
    #         'password': 123
    #     }
    #     response = self.client.post(url, data=data)
    #
    #     self.assertEqual(response.status_code, 400)
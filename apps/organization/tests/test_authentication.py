#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.tests.test_authentication
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

User = get_user_model()


MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class UserAuthenticationTestCase(TestCase):
    """Handles User Authentication Test Cases

    """

    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.user.set_password('123456')
        self.user.save()

    def test_login(self):
        """Test User Login with Valid credentials

        """
        url = reverse('accounts:user-login')
        data = {
            'email': 'test@example.com',
            'password': '123456'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 200)

    def test_wrong_login(self):
        """Test User Login with In-Valid credentials

        """
        url = reverse('accounts:user-login')
        data = {
            'email': 'test@example.com',
            'password': 'abcdef'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 401)

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- accounts.tests.test_models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
class UserTestCase(TestCase):
    """Handles User Views Test Cases

    """

    def setUp(self):
        self.image = self._create_temp_image()
        self.user = User.objects.create(email='test@example.com')

    def _create_temp_image(self):
        """

        :return: image object
        """
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', (200, 200), 'white')
            image.save(f, 'PNG')

        return open(f.name, mode='rb')

    def tearDown(self):
        self.image.close()

    def test_user_create(self):
        """Test Create User Object

        """
        url = reverse('accounts:user-create')
        data = {
            'email': 'test-m3@example.com',
            'avatar': self.image,
            'password': 123
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)

    def test_user_detail(self):
        """Test User Object details

        """
        url = reverse('accounts:user-detail', args=(self.user.uuid, ))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_user_update(self):
        """Test Update User Object

        """
        url = reverse('accounts:user-detail', args=(self.user.uuid, ))
        data = urlencode({
            'name': 'updated-test'
        })
        response = self.client.patch(url, content_type="application/x-www-form-urlencoded", data=data)

        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        """Test Delete Update User Object

        """
        url = reverse('accounts:user-detail', args=(self.user.uuid, ))

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

    def test_shadow_user(self):
        """Test Shadow User Create

        """
        url = reverse('accounts:get-or-create-shadow-user')
        data = {
            'email': 'test-m4@example.com',
            'avatar': self.image,
            'password': 123,
            'is_active': False
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 201)

    def test_user_email_unique(self):
        """Test User with same email doesn't get created.

        """
        url = reverse('accounts:user-create')
        data = {
            'email': 'test@example.com',
            'avatar': self.image,
            'password': 123
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 400)
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-24 06:32
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_organization_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Organization uuid, this token will uniquely identify Organization.', unique=True, verbose_name='Organization Unique Identifier'),
        ),
    ]

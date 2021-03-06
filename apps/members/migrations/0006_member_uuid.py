# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-27 08:54
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0005_member_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Member uuid, this token will uniquely identify Member.', unique=True, verbose_name='Member Unique Identifier'),
        ),
    ]

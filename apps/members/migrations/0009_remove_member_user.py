# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20170726_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='user',
        ),
    ]

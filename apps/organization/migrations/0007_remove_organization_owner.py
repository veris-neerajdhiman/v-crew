# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-26 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20170726_1137'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='owner',
        ),
    ]
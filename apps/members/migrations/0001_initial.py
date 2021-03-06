# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 11:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0002_auto_20170420_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Required. 64 characters or fewer.', max_length=64, verbose_name='Member Name')),
                ('email', models.EmailField(help_text='Primary Contact of Member, immutable.', max_length=254, verbose_name='Member Email.')),
                ('type', models.BooleanField(choices=[('terminal', 'terminal'), ('user', 'user')], help_text='Member type, for internal user only', verbose_name='Member type.')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Organization Creation time.')),
                ('modified_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Organization Modification time.')),
                ('organization', models.ForeignKey(help_text='Member Organization.', on_delete=django.db.models.deletion.CASCADE, to='organization.Organization')),
            ],
            options={
                'verbose_name': 'Organization Member',
                'ordering': ['-id'],
                'verbose_name_plural': 'Organization Members',
            },
        ),
        migrations.AlterUniqueTogether(
            name='member',
            unique_together=set([('email', 'organization')]),
        ),
    ]

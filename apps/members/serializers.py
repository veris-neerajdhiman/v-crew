#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.member.serializers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- This file contains member micro-service models.
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

# Django

# local

# own app
from apps.members import models, config


class MemberSerializer(serializers.ModelSerializer):
    """This Serializer is used when we qil retrieve, update a Member.

    """
    class Meta:
        model = models.Member
        exclude = ('created_at', 'modified_at', )
        read_only_fields = ('id', 'email', )


class MemberAddSerializer(serializers.ModelSerializer):
    """This Serializer is used when we are adding a Member.

    """
    email = serializers.EmailField(required=False,)
    type = serializers.ChoiceField(required=True,
                                   choices=config.MEMBER_TYPES)

    class Meta:
        model = models.Member
        exclude = ('created_at', 'modified_at', )
        validators = [
           UniqueTogetherValidator(
                queryset=models.Member.objects.all(),
                fields=('email', 'organization', )
           )
        ]

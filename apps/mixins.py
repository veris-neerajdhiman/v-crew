#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.mixins
~~~~~~~~~~~~~~

- This file includes custom mixins to customize Behaviour of any existing class
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django

# local

# own app


class MultipleFieldLookupMixin(object):
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    def get_queryset(self):
        """

        """
        queryset = self.queryset  # Get the base queryset
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        return queryset.filter(**filter)

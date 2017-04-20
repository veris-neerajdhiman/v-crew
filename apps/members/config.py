#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- apps.members.config
~~~~~~~~~~~~~~

- This file holds the general settings of Member micro-services.
 """

# django

MAXLENGTH = 8
TERMINAL = 'terminal'
USER = 'user'

MEMBER_TYPES = (
    (TERMINAL, TERMINAL),
    (USER, USER),
)

#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
- auth.jwt
~~~~~~~~~~

- This file contains Functions of Generating and Validating JWT (json web tokens)
"""


# future
from __future__ import unicode_literals

# 3rd party
import jwt


def create_jwt(payload, secret, algo):
    """

    :param payload: Payload you want to encrypt.
    :param secret: Public key used to encrypt
    :param algo: Algorithm used to encrypt
    :return: json web token
    """

    return jwt.encode(payload, secret, algorithm=algo)


def validate_jwt(token, secret, aud, verify=True):
    """

    :param token: json web token
    :param secret: Public key used to decrypt jwt
    :param aud: JWT Audience
    :param verify: Verify JWT ?
    :return: Decrypted JWT
    """
    return jwt.decode(token, secret, audience=aud, verify=verify)

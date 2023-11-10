#!/usr/bin/env python3
"""API session authentication"""


from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """
    a class that uses session to authenticate users
    """
    pass

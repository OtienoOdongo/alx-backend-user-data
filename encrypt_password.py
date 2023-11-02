#!/usr/bin/env python3
"""
Encrypting passwords using the bcrypt package
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashing a password using bcrypt.

    Args:
    - password (str): The plain text password to be hashed.

    Returns:
    - bytes: The hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Checking if a plain text password matches a hashed password.

    Args:
    - hashed_password (bytes): The hashed password to be validated.
    - password (str): The plain text password to be checked.

    Returns:
    - bool:
    True if the plain text password matches the hashed password,
    False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

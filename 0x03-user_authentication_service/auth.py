#!/usr/bin/env python3
"""
authenticating modules
"""


import bcrypt
from db import DB
from user import User
import uuid
from typing import Union
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> str:
    """
    Hashing a password using bcrypt with a random salt.

    Parameters:
        password(str): The passwrd to be hashed.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generating a random salt
    rand_salt = bcrypt.gensalt()

    # Hashing the password with the generated salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), rand_salt)

    return hashed_password


def _generate_uuid() -> str:
    """
    Generating a new UUID

    Returns:
        str: a string representation of the new UUID
    """
    new_uuid = uuid.uuid4()
    return str(new_uuid)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hashing a password using bcrypt with a random salt.

        Parameters:
            password(str): The passwrd to be hashed.

        Returns:
            bytes: The salted hash of the password.
        """
        # Generating a random salt
        rand_salt = bcrypt.gensalt()

        # Hashing the password with the generated salt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), rand_salt)

        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Registering a new user if its details does not exist in the db

        Parameters:
            email (str): The email of the user
            password (str): The password of the user

        Returns:
            User:
                User object for the registered user.

        Raises:
            ValueError:
                If a user with the provided email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            # If the user exists, raise a ValueError
            raise ValueError(f"User {email} already exists.")

        except NoResultFound:
            # If NoResultFound exception is caught,
            # and proceed with user registration
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checking if the provided credentials are valid.

        Args:
            email (str):
                The email of the user.
            password (str):
                The password to be checked.

        Returns:
            bool:
                True if the credentials are valid
                False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> Union[str, None]:
        """
        Creating a new session for the user

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.
        """
        try:
            # Finding the user by email
            user = self._db.find_user_by(email=email)

            # Generating a new session ID
            session_id = _generate_uuid()

            # Then updating the user's session_id in the database
            self._db.update_user(user.id, session_id=session_id)
            # Return the session ID
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Get the corresponding user for a given session ID.

        Args:
            session_id (str):
                The session ID to look up.

        Returns:
            Union[User, None]:
                The corresponding User or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Updating the corresponding user's session ID to None.

        Args:
            user_id (int):
            The user ID whose session should be destroyed.
        """
        return self._db.update_user(user_id, session_id=None)

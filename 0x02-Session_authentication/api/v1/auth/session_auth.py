#!/usr/bin/env python3
"""API session authentication"""


from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    a class that uses session to authenticate users
    """
    # Class attribute to store user_id by session_id
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creating a Session ID for a user_id.

        Args:
            user_id (str):
            The user's ID to associate with the session.

        Returns:
            str:
            A generated Session ID or None.
        """
        if user_id is None or type(user_id) is not str:
            return None

        # Generating a Session ID using uuid4
        session_id = str(uuid.uuid4())

        # Storing the user_id in the dictionary using session_id as the key
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieving a User ID based on a Session ID.

        Args:
            session_id (str):
            The Session ID to look up the associated User ID.

        Returns:
            str:
            The User ID associated with the given Session ID,
            it returns None if not found.
        """
        if session_id is None or type(session_id) is not str:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returning a User instance based on a cookie value.

        Returns:
            TypeVar('User'):
            The User instance if authenticated
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

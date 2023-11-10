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

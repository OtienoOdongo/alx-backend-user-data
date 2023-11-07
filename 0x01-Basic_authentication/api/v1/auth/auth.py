#!/usr/bin/env python3
"""
a class that manages API authentication
its template for all authentication system
that will be implemented
"""


from flask import request
from typing import List, TypeVar


class Auth:
    """API authentication management"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checking if authentication is required for the given path.

        Args:
            path (str):
            The path to check for authentication requirement.
            excluded_paths (List[str]):
            A list of paths that are excluded from authentication.

        Returns:
            bool:
            True if authentication is required, False otherwise.
        """
        # Check if path is None or excluded_paths is None or empty
        if path is None or not excluded_paths:
            return True

        # Add a trailing slash to the path if it doesn't have one
        if not path.endswith('/'):
            path += '/'

        # Iterate through excluded_paths and check if path is in it
        for excluded_path in excluded_paths:
            if excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Getting the authorization header from the request.

        Args:
            request (Request):
            The Flask request object.

        Returns:
            str:
            The authorization header if present
            otherwise return None.
        """
        if request is None:
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Getting the current user based on the request.

        Args:
            request (Request):
            The Flask request object.

        Returns:
            TypeVar('User'):
            The current user if authenticated
            otherwise return None.
        """
        return None

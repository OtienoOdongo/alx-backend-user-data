#!/usr/bin/env python3
"""
a BasicAuth class that inherits from Auth
"""


from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar, Union


class BasicAuth(Auth):
    """
    a BasicAuth class that inherits from Auth
    """
    def extract_base64_authorization_header(
        self,
        authorization_header: str
    ) -> str:
        """
        Extract the Base64-encoded credentials
        from a Basic Authentication header.

        Args:
            authorization_header (str):
                Authorization header string containing
                Basic Authentication credentials.

        Returns:
            str:
                The Base64 part of the Authorization
                header for Basic Authentication.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith('Basic ')
        ):
            return None

        # Extracting the Base64 part after 'Basic '
        base64_encoded = authorization_header[len('Basic '):]
        return base64_encoded

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """
        Decoding a Base64-encoded authorization header and
        returning the decoded value as a UTF-8 string.

        Args:
            base64_authorization_header (str):
                A Base64-encoded authorization header.

        Returns:
            str:
                The decoded value of a Base64 string as a UTF-8 string
        """
        # Checking if base64_authorization_header is None or not a string
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            # Decoding the Base64 data and converting it into a UTF-8 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> Tuple[str]:
        """
        Extracting user email and password
        from a decoded Base64 authorization header.

        Args:
        decoded_base64_authorization_header (str):
            The decoded Base64 authorization header.

        Returns:
        tuple:
            A tuple containing user email and
            user password as (email, password),
            or (None, None) if the input is invalid.
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
        ):
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        email, password = decoded_base64_authorization_header.split(':', 1)
        return (email, password)

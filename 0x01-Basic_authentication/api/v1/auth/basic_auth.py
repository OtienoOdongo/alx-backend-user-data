#!/usr/bin/env python3
"""
a BasicAuth class that inherits from Auth
"""


from api.v1.auth.auth import Auth


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
            decoded_bytes = base64.b64decode(
                base64_authorization_header).decode('utf-8')
            return decoded_bytes
        except Exception:
            return None

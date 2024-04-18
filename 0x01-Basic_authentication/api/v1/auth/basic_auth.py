#!/usr/bin/env python3
"""

"""
from base64 import b64decode
from typing import Optional
from auth import Auth


class BasicAuth(Auth):
    """
    Handles basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        in the class BasicAuth that
        returns the Base64 part of the
        Authorization header for
        a Basic Authentication:
        """

        if authorization_header is None:
            return

        if not isinstance(authorization_header, str):
            return

        if not authorization_header.startswith('Basic '):
            return

        value = authorization_header.split(' ')[1]
        return value

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        returns the decoded value of a Base64 string base64_authorization_header
        """
        if not base64_authorization_header:
            return

        if not isinstance(base64_authorization_header, str):
            return

        try:

            encoded_base64 = b64decode(base64_authorization_header)
            decoded_base64 = encoded_base64.decode('utf-8')
        except Exception:
            return
        return decoded_base64

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Optional[tuple[str, str]]:
        """
        Return None, None if decoded_base64_authorization_header is None
        Return None, None if decoded_base64_authorization_header is not a string
        Return None, None if decoded_base64_authorization_header doesn’t contain
        Return the user email and the user password separated by :
        """


if __name__ == '__main__':
    a = BasicAuth()

    print(a.decode_base64_authorization_header(None))
    print(a.decode_base64_authorization_header(89))
    print(a.decode_base64_authorization_header("Holberton School"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9u"))
    print(a.decode_base64_authorization_header("SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.decode_base64_authorization_header(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA==")))

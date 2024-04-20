#!/usr/bin/env python3
"""

"""
from base64 import b64decode
import uuid
from typing import Optional, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


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
        if not decoded_base64_authorization_header:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user, pwd = decoded_base64_authorization_header.split(':')
        return user, pwd

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance
        based on his email and password
        """

        if not user_email or not isinstance(user_email, str):
            return

        if not user_pwd or not isinstance(user_pwd, str):
            return

        try:
            users = User.search(attributes={"email": user_email})
        except KeyError:
            return
        except Exception:
            return

        if not users:
            return
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return


if __name__ == '__main__':
    """create a user test"""
    user_email = str(uuid.uuid4())
    user_clear_pwd = str(uuid.uuid4())
    user = User()
    user.email = user_email
    user.first_name = "Bob"
    user.last_name = "Dylan"
    user.password = user_clear_pwd
    print("New user: {}".format(user.display_name()))
    user.save()

    """retrieve user via class BasicAuth"""

    a = BasicAuth()

    u = a.user_object_from_credentials(None, None)
    print(u.display_name() if u is not None else "None")
    
    u = a.user_object_from_credentials(89, 98)
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials("email@notfound.com", "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, "pwd")
    print(u.display_name() if u is not None else "None")

    u = a.user_object_from_credentials(user_email, user_clear_pwd)
    print(u.display_name() if u is not None else "None")

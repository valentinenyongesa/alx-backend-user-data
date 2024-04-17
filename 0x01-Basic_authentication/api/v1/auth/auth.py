#!/usr/bin/env python3
"""
Auth class

"""
from flask import request
from typing import List


class Auth:
    """This class is the
    template for all authentication
    system you will implement
    """


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        defining the class
        """
        return False

    def authorization_header(self, request=None) -> None:
        """
        returns None - request will be 
        the Flask request object
        """
        return

    def current_user(self, request=None) -> None:
        """
        returns None - request will be
        the Flask request object
        """
        return


if __name__ == '__main__':
    a = Auth()


    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.authorization_header())
    print(a.current_user())

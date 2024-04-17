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
        if path and not path.endswith('/'):
            path = path + '/'
        """Returns True if path is None"""
        if not path or path not in excluded_paths:
            return True
        """Returns True if excluded_paths is None or empty"""
        if not excluded_paths or excluded_paths == []:
            return True
        """Returns False if path is in excluded_paths"""
        if path in excluded_paths:
            return False
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

    print(a.require_auth(None, None))
    print(a.require_auth(None, []))
    print(a.require_auth("/api/v1/status/", []))
    print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))
    print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))
    print(
          a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"])
          )

#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    takes in a password string
    arguments and returns bytes
    """
    encoded_pwd = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)

    return hashed_pwd


if __name__ == '__main__':
    print(_hash_password("password"))

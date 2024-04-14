#!/usr/bin/env python3
"""
Module to securely hash passwords using bcrypt.
"""

import bcrypt
from typing import Union


def hash_password(password: str) -> bytes:
    """
    Hashes the input password using bcrypt with a randomly generated salt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password


if __name__ == "__main__":
    # Example usage: hash the password "MyAmazingPassw0rd"
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password.decode())  # Convert bytes to string for output

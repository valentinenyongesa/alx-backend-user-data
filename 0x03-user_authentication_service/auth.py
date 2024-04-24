#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""

import bcrypt
from sqlalchemy.exc import NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    takes in a password string
    arguments and returns bytes
    """
    encoded_pwd = password.encode("utf-8")

    salt = bcrypt.gensalt()

    hashed_pwd = bcrypt.hashpw(encoded_pwd, salt)

    return hashed_pwd


class Auth:
    """
    interacts with authentication database
    """

    def __init__(self) -> None:
        """
        Initialize Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user
        """
        try:
            existing_user = self._db.find_user_by(email=email)

            if existing_user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_pwd = _hash_password(password)

        new_usr = self._db.add_user(email=email,
                                    hashed_password=hashed_pwd.decode("utf-8"))
        self._db
        return new_usr

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate user login credential
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                encoded_hashed_pwd = password.encode()
                user_pwd_bytes = existing_user.hashed_password.encode('utf-8')
                return bcrypt.checkpw(encoded_hashed_pwd, user_pwd_bytes)
            else:
                return False
        except NoResultFound:
            return False


if __name__ == '__main__':
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth = Auth()

    auth.register_user(email, password)

    print(auth.valid_login(email, password))

    print(auth.valid_login(email, "WrongPwd"))

    print(auth.valid_login("unknown@email", password))

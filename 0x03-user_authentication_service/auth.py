#!/usr/bin/env python3
"""
Module to hash password and interact with auth DB
"""

import uuid
import bcrypt
from sqlalchemy.exc import NoResultFound
from typing import Optional
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


def _generate_uuid() -> str:
    """
    string representaion of uuid
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> Optional[str]:
        """
        Takes an email string
        argument and returns the
        session ID as a string
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(existing_user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[str]:
        """
        Find user by session ID
        """
        try:
            existing_user = self._db.find_user_by(session_id=session_id)
            if existing_user:
                return existing_user
            return
        except Exception:
            return


if __name__ == '__main__':
    pass

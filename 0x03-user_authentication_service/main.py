#!/usr/bin/env python3
"""
Request module
"""


import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

BASE_URL = "http://localhost:5000/"


def register_user(email: str, password: str) -> None:
    """
    Test for va;lidating user registration
    """
    data = {"email": email,
            "password": password}

    response = requests.post(BASE_URL + "users", data=data)

    message = {"email": email, "message": "user created"}

    assert response.status_code == 200

    assert response.json() == message


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test for validating login
    with wrong oassword
    """
    data = {"email": email, "password": "word_password"}
    response = requests.post(BASE_URL + "sessions", data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    To validate successful login
    """
    data = {"email": email,
            "password": password}

    response = requests.post(BASE_URL + "SESSIONS", data=data)
    message = {"email": email, "message": "logged in"}
    assert response.status_code == 200
    assert response.json() == message

    session_id = response.cookies.get("session_id")
    return session_id


def profile_unlogged() -> None:
    """
    validating profile request without log in
    """
    cookies = {"session_id": "fake_session_id"}
    response = requests.get(BASE_URL + "profile", cookies=cookies)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    validating profile request loged in
    """
    cookies = {"session_id": session_id}
    response = requests.get(BASE_URL + "profile", cookies=cookies)
    message = {"email": EMAIL}
    assert response.status_code == 200
    assert response.json() == message


def log_out(session_id: str) -> None:
    """
    validating logout endpoint
    """
    cookies = {"session_id": session_id}
    response = requests.delete(BASE_URL + "sessions", cookies=cookies)
    message = {"message": "Bienvenue"}
    assert response.status_code == 200
    assert response.json() == message


def reset_password_token(email: str) -> str:
    """
    test for validating paswd reset token
    """
    response = requests.post(BASE_URL + "reset_password", data=data)
    assert response.status_code == 200
    reset_token = response.json().get("reset_token")
    message = {"email": email, "reset_token": reset_token}
    assert response.json() == message
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    valdating password reset update
    """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(BASE_URL + "reset_password", data=data)
    message = {"email": email, "message": "Password updated"}
    assert response.status_code == 200
    assert response.json() == message


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)

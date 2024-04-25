#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import (Flask, jsonify, Response,
                   request, abort, make_response,
                   redirect)
from typing import Optional, Tuple
from auth import Auth


AUTH = Auth()

app = Flask(__name__)


@app.route("/")
def home() -> Response:
    """
    Route to home
    """
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route("/users", methods=["POST"])
def users() -> Response:
    """
    Implement the end point to regisre
    user
    """
    if request.method == "POST":
        raw_email = request.form.get("email")
        email = raw_email.strip()
        raw_password = request.form.get("password")
        password = raw_password.strip()
        try:
            AUTH.register_user(email, password)
            message = jsonify({"email": email,
                               "message": "user_created"})
            return message
        except Exception:
            return jsonify({"message": "email already registered"})
    else:
        abort(400)


@app.route("/session", methods=["POST"])
def login() -> Optional[Tuple]:
    """
    implement a login function
    to respond to the POST /sessions route
    """
    try:
        if request.method == "POST":
            raw_email = request.form.get("email")
            email = raw_email.strip()
            raw_password = request.form.get("password")
            password = raw_password.strip()
            try:
                if not AUTH.valid_login(email, password):
                    abort(401)
                session_id = AUTH.create_session(email)
                message = {"email": email, "message": "logged in"}
                response = make_response(jsonify(message), 200)
                response.set_cookie("session_id", session_id)
                return response
            except ValueError:
                abort(401)
        else:
            abort(401)
    except Exception:
        abort(401)


@app.route("/sessions", methods=["DELETE"])
def logout() -> Response:
    """
    implement a logout function to
    respond to the DELETE /sessions route
    """
    if request.method == "DELETE":
        session_id = request.cookies.get("session_id", None)
        if session_id is None:
            abort(403)
        try:
            existing_user = AUTH.get_user_from_session_id(session_id)
            if existing_user:
                AUTH.destroy_session(existing_user.id)
                return redirect("/")
        except Exception:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

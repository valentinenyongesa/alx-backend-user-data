#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, Response, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

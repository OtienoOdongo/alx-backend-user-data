#!/usr/bin/env python3
"""
Basic Flask app
"""


from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
from typing import Union


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    A GET route that returns Bienvenue a French word
    meaning welcome in English

    Return:
        dict: JSON payload.
    """
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def user_registration() -> str:
    """
    A POST route endpoint for registering new users

    Returns:
        dict: JSON payload.
    """
    try:
        email = request.form.get('email')
        password = request.form.get('password')

        # Using AUTH to register the user
        new_user = AUTH.register_user(email, password)

        # It indicates that the User has been registered successfully
        return jsonify(
            {"email": new_user.email, "message": f"user created"}
        ), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    A POST route that handles login functionality

    Returns:
        str: JSON response with a message if successfull
        (session id cookie)
    """
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if not valid_login:
        abort(401)
    session_id = AUTH.create_session(email)
    response = jsonify({"email": f"{email}", "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> Union[str, None]:
    """
    A DELETE route that logs out the user
    and destroys the user's session.

    Returns:
        Response: redirected to the default route(/)
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> Union[str, None]:
    """
    A GET /profile
    Responds with user profile information if the session ID is valid.

    Returns:
        - JSON payload with user email if session is valid (200 status)
        - 403 status if the session ID is invalid or the user does not exist.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    POST /reset_password
    Generating a reset password token for the user.

    Returns:
        JSON: {"email": "<user email>", "reset_token": "<reset token>"}
    """
    email = request.form.get('email')
    user = AUTH.create_session(email)

    if not user:
        abort(403)
    else:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{reset_token}"})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Updating the user's password using the provided reset token.

    The request is expected to contain form data with fields
    "email", "reset_token", and "new_password".

    Returns:
        Response: updated Password or 403 if the token is invalid
    """
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        # Updating the password using Auth.update_password
        AUTH.update_password(reset_token, new_password)

        updated_data = {"email": email, "message": "Password updated"}
        return jsonify(updated_data), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

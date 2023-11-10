#!/usr/bin/env python3
"""
a module defining all session authentication routes
"""


import os
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    This module handles user login using Session authentication.

    It retrieves user data from a form POST request
    (POST /api/v1/auth_session/login)
    It then validates the request
    afterwhich it sets a session cookie for the user.

    Returns:
        JSON response:
        The user data or an error message with appropriate status codes.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user_being_searched = User.search({"email": email})

    if not user_being_searched:
        return jsonify({"error": "no user found for this email"}), 404

    if not user_being_searched[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session_name = os.getenv("SESSION_NAME")
    session_id = auth.create_session(user_being_searched[0].id)
    response = make_response(jsonify(user_being_searched[0].to_json()))

    if session_name and session_id:
        response.set_cookie(session_name, session_id)
    return response


@app.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    This method Logs out the user by destroying their session.

    Returns:
        tuple:
        An empty JSON dictionary
        and a status code 200 on success or 404 on failure
    """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200

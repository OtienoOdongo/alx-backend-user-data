#!/usr/bin/env python3
"""
Basic Flask app
"""


from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")

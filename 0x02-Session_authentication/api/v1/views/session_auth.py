#!/usr/bin/env python3
"""Module handles all routes for Session Authentication"""

import os
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from typing import Tuple


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    no_user = {"error": "no user found for this email"}

    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(no_user), 404
    if len(users) <= 0:
        return jsonify(no_user), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sesh_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), sesh_id)
        return res
    return jsonify({"error": "wrong password"}), 401


@app_views.route(
        '/auth_session/logout',
        methods=['DELETE'],
        strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})

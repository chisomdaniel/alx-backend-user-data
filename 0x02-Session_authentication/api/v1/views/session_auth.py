#!/usr/bin/env python3
'''New view for session auth'''
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_login() -> str:
    '''New view for Session Authentication  that handles all
    routes for the Session authentication'''

    user_details = request.form
    if user_details.get('email', None) in (None, ''):
        return jsonify({"error": "email missing"}), 400
    if user_details.get('password', None) in (None, ''):
        return jsonify({"error": "password missing"}), 400

    all_user = User.search({'email': user_details.get('email')})
    if not all_user or all_user == []:
        return jsonify({"error": "no user found for this email"}), 404

    user = None
    for i in all_user:
        if i.is_valid_password(user_details.get('password')):
            user = i
            break

    if user is None:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    session = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME", None)

    resp = jsonify(user.to_json())
    resp.set_cookie(session_name, session)
    return resp


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    '''logout session'''
    from api.v1.app import auth
    if not auth.destroy_session(request):
        return False, abort(404)

    return jsonify({}), 200

#!/usr/bin/env python3
'''basic flask app'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def basic() -> str:
    '''a basic route'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    '''creates a new user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    '''implement a login function'''
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
    else:
        abort(401)

    output = jsonify({"email": email, "message": "logged in"})
    output.set_cookie('session_id', session_id)
    return output


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> None:
    '''implement a logout function'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        return redirect('/')
    else:
        abort(403)


@app.route('/profile', strict_slashes=False)
def profile() -> str:
    '''profile function'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    '''get reset password token'''
    email = request.form.get('email')
    if email is None:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    '''update the user password'''
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    password = request.form.get('password')
    if not email or not reset_token or not password:
        abort(403)
    try:
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")

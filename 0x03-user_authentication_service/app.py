#!/usr/bin/env python3
'''basic flask app'''
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def basic() -> str:
    '''a basic route'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
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


@app.route('/sessions', methods=['POST'])
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


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''implement a logout function'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    
    user = AUTH.get_user_from_session_id(session_id)
    if user is not None:
        AUTH.destroy_session(user.id)
        redirect('/')
    else:
        abort(403)


@app.route('/profile')
def profile():
    '''profile function'''
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    
    return jsonify({"email": user.email})



if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")

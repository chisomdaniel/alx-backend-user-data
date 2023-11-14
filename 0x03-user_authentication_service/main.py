#!/usr/bin/env python3
'''main file'''
import requests


url = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    '''register a new user'''
    resp1 = {'email': email, 'message': 'user created'}
    resp2 = {"message": "email already registered"}
    data = {'email': email, 'password': password}
    r = requests.post(url+'/users', data=data)
    assert r.status_code in (200, 400)
    assert r.json() == resp1 or resp2


def log_in_wrong_password(email: str, password: str) -> None:
    '''log in wrong password'''
    data = {'email': email, 'password': password}
    r = requests.post(url+'/sessions', data=data)
    print(r.status_code)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    '''login function'''
    data = {'email': email, 'password': password}
    resp = {'email': email, 'message': 'logged in'}
    r = requests.post(url+'/sessions', data=data)
    assert r.status_code == 200
    assert r.json() == resp

    session_id = r.cookies.get('session_id')
    # print(session_id)
    return session_id


def profile_unlogged() -> None:
    '''profile unlogged'''
    r = requests.get(url+'/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    '''login with session_id'''
    # print(session_id)
    r = requests.get(url+'/profile', cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.json() == {'email': 'guillaume@holberton.io'}  # confirm


def log_out(session_id: str) -> None:
    '''log out'''
    r = requests.delete(url+'/sessions', cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''reset password token'''
    data = {'email': email}
    r = requests.post(url+'/reset_password', data=data)
    out = r.json()
    assert r.status_code == 200
    assert r.json() == {"email": email, "reset_token": out.get('reset_token')}
    return out.get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {'email': email, 'reset_token': reset_token,
            'password': new_password}
    r = requests.put(url+'/reset_password', data=data)
    assert r.json() == {"email": email, "message": "Password updated"}
    assert r.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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

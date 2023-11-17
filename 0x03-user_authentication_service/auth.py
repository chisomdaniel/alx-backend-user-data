#!/usr/bin/env python3
'''hash password'''
import bcrypt
from db import DB
from typing import Any
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    '''hash password'''
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    '''generate a uuid'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''regester a user'''
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError("User <{}> already exists".format(user.email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        # except InvalidRequestError:
        #    pass

    def valid_login(self, email: str, password: str) -> bool:
        '''validate a login'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        user_pwd = user.hashed_password

        input_pwd = password.encode('utf-8')

        result = bcrypt.checkpw(input_pwd, user_pwd)
        return result

    def _generate_uuid(self) -> str:
        '''generate a uuid'''
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        '''create a session id for a given user'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        # print(user, user.email, user.session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str = None) -> User:
        '''get user from session id'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        '''destroy a session given a session id'''
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None

        return None

    def get_reset_password_token(self, email: str) -> str:
        '''generate a reset password token'''
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        '''update password function'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed,
                             reset_token=None)
        return None

#!/usr/bin/env python3
'''SessionAuth implementation'''
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    '''SessionAuth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create a session'''
        if user_id is None:
            return None
        if type(user_id).__name__ != 'str':
            return None

        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''retreive a user ID'''
        if session_id is None:
            return None
        if type(session_id).__name__ != 'str':
            return None

        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''override the current_user inherited method'''
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        '''delete a session'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False

        del SessionAuth.user_id_by_session_id[session_id]
        return True

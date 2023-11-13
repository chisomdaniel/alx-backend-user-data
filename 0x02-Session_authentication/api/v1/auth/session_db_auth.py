#!/usr/bin/env python3
'''sessions in database'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    '''session db class'''

    def create_session(self, user_id=None):
        '''create a new session'''
        session_id = super().create_session(user_id)
        new_session = UserSession(user_id, session_id)
        new_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''get user is for the session id given'''
        return super().user_id_for_session_id(session_id)

    def destroy_session(self, request=None):
        '''destroy session'''
        rtn = super().destroy_session(request)
        SessionDBAuth.save_to_file()
        return rtn

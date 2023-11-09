#!/usr/bin/env python3
'''Session expiration module'''
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


duration = getenv("SESSION_DURATION", None)


class SessionExpAuth(SessionAuth):
    '''session exp auth class'''
    def __init__(self):
        try:
            self.session_duration = int(duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''create a new session with a date'''
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        user_id = super().user_id_for_session_id(session_id)
        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.now()}
        super().user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''return the user id given the session id'''
        if session_id is None:
            return None
        if super().user_id_by_session_id.get(session_id, None) is None:
            return None
        user_id = super().user_id_by_session_id.get(session_id
                                                    ).get('user_id',
                                                          None)
        if user_id is None:
            return None
        if self.session_duration <= 0:
            return user_id
        print(super().user_id_by_session_id)
        created_at = super().user_id_by_session_id.get(session_id
                                                       ).get('created_at',
                                                             None)
        if created_at is None:
            return None
        dt = timedelta(seconds=self.session_duration)
        dt_sum = created_at + dt
        if dt_sum < datetime.now():
            return None
        return user_id

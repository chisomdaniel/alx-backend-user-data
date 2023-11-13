#!/usr/bin/env python3
'''session in database'''
from models.base import Base


class UserSession(Base):
    '''user session class'''
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = ""
        self.session_id = ""

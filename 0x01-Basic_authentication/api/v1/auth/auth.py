#!/usr/bin/usr python3
'''contains the class to manage the API authentication'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''manages the API authentication'''

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require auth function'''
        if path is None:
            return True
        if excluded_paths is None:
            return True

        if path[-1] != '/':
            path = path+'/'

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''auth header'''
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None

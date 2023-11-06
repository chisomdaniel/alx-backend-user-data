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

        for i in excluded_paths:
            if i[-1] == '*':
                new_ex = i.split('/')
                new_path = path.split('/')

                if '/'.join(new_path[:-2]) == '/'.join(new_ex[:-1]):
                    new_ex2 = new_ex[-1].replace('*', '')
                    new_path2 = new_path[-2]
                    if new_path2.startswith(new_ex2):
                        return False

        if path in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        '''auth header'''
        if request is None:
            return None

        header = request.headers.get('Authorization', None)
        if header is None:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        '''current user'''
        return None

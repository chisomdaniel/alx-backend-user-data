#!/usr/bin/env python3
'''Basic auth file'''
from api.v1.auth.auth import Auth
from base64 import b64decode
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    '''Basic auth class'''

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None:
            return None

        if type(authorization_header).__name__ != 'str':
            return None

        header = authorization_header.split(' ')
        if header[0] != 'Basic':
            return None

        return header[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        '''decode the base64 encoding'''
        if base64_authorization_header is None:
            return None

        if type(base64_authorization_header).__name__ != 'str':
            return None

        try:
            string = b64decode(base64_authorization_header).decode("utf-8")
        except Exception as e:
            return None

        return string

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        '''extract and return the user email and password'''
        if decoded_base64_authorization_header is None:
            return None, None

        if type(decoded_base64_authorization_header).__name__ != 'str':
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        details = decoded_base64_authorization_header.split(':', 1)

        return details[0], details[1]

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        '''return user object from the given credentials'''
        if user_email is None or type(user_email).__name__ != 'str':
            return None
        if user_pwd is None or type(user_pwd).__name__ != 'str':
            return None

        try:
            users = User.search({'email': user_email})
        except KeyError:
            return None

        for i in users:
            if i.is_valid_password(user_pwd):
                return i

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''retrieves the User instance for a request'''
        header = self.authorization_header(request)
        encoded, decoded, email, passwd = None, None, None, None
        if header is not None:
            encoded = self.extract_base64_authorization_header(header)
        if encoded:
            decoded = self.decode_base64_authorization_header(encoded)
        if decoded:
            email, passwd = self.extract_user_credentials(decoded)
        if email and passwd:
            usr_obj = self.user_object_from_credentials(email, passwd)

            return usr_obj

        return None

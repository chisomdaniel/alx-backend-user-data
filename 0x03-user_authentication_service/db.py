#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        # change echo back to True
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''add a user to the db'''
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''find a user by a property'''
        session = self._session
        if not kwargs:
            raise InvalidRequestError
        for key in kwargs.keys():
            if key not in User.__table__.columns.keys():
                raise InvalidRequestError
        user = session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound

        return user

    def update_user(self, user_id: str, **kwargs: dict) -> None:
        '''update a user'''
        user = self.find_user_by(id=user_id)
        attr_list = ['id', 'email', 'hashed_password',
                     'session_id', 'reset_token']
        for key, value in kwargs.items():
            if key not in attr_list:
                raise ValueError
            setattr(user, key, value)
        self._session.commit()

#!/usr/bin/env python3
"""
DB module

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
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """
        creating/adding a new user to the db
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        self._session.refresh(new_user)
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Finding a user with a given set of attributes.

        Returns:
            User: User if found.

        Raises:
            NoResultFound: When no user is found.
        """
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found with the specified attributes.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:

        """
        Updating details of an existing user.

        Returns:
            None

        Raises:
            ValueError: If an invalid attribute is passed.
        """
        user_details = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if hasattr(user_details, key):
                setattr(user_details, key, val)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.commit()

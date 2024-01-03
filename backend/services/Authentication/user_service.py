"""Service layer for the user module."""
from fastapi import Depends
from ...database import db_session

from ...models.Authentication.user import User

class UserService():
    """Class to perform all actions on the user table in the database."""

    def __init__(self,
                session = Depends(db_session),
    ):
        self._session = session

    def fake_decode_token(token: str):
        return User(
            username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
        )

    def get_current_user(self, token: str):
        user = self.fake_decode_token(token=self._token)
        return user
    
    def login()
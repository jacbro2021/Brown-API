"""Service layer for the user module."""
from fastapi import Depends
from ...database import db_session

from ...models.Authentication.user import User
from ...entities.Authentication.user_entity import UserEntity

from typing import Dict
from sqlalchemy import select

class UserService():
    """Class to perform all actions on the user table in the database."""

    def __init__(self,
                session = Depends(db_session),
    ):
        self._session = session

    def fake_decode_token(self, token: str):
        """Fake helper to decode token"""
        query = select(UserEntity).where(UserEntity.username == token)
        ent: UserEntity | None = self._session.scalar(query)
        if ent ==  None:
            # TODO: Throw custom exception here.
            raise Exception("User not found.")
        
        return ent.to_model()
    
    def fake_hash_password(self, password: str) -> str:
        """Fake helper function to hash password."""
        return "fakehash" + password

    def get_current_user(self, token: str):
        """TODO: Add documentation here."""
        user = self.fake_decode_token(token=self._token)
        return user
    
    async def get_current_active_user(self, token: str):
        """TODO: Add documentation here."""
        current_user = self.get_current_user(token)

        if current_user.disabled:
            # TODO: Raise custom exception here.
            raise Exception("User is disabled.")
        return current_user
    
    def login(self, username: str, plain_password: str) -> Dict[str, str]:
        """TODO: Add documentation here"""
        # Find user with the given username.
        query = select(UserEntity).where(UserEntity.username == username)
        user_entity = self._session.scalar(query)

        if not user_entity:
            # TODO: Raise custom exception here.
            raise Exception("User not found")
        
        # Check password correctness.
        hashed_password = self.fake_hash_password(password=plain_password)
        if hashed_password != user_entity.hashed_password:
            #TODO: Raise custom exception here.
            print("wrong password")
            raise Exception("Incorrect username or password.")
        
        return {"access_token": user_entity.username, "token_type": "bearer"}

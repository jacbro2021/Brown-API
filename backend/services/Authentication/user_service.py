"""Service layer for the user module."""
from fastapi import Depends
from ...database import db_session

from ...models.Authentication.user import User
from ...entities.Authentication.user_entity import UserEntity

from typing import Dict
from sqlalchemy import select
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from ...env import getenv

class UserService():
    """Class to perform all actions on the user table in the database."""

    def __init__(self,
                session = Depends(db_session),
    ):
        self._session = session
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._SECRET_KEY = getenv("JWT_SECRET")
        self._ALGORITHM = "HS256"
        self._ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def get_user(self, username: str) -> User:
        """Fake helper to decode token"""
        query = select(UserEntity).where(UserEntity.username == username)
        ent: UserEntity | None = self._session.scalar(query)
        if ent ==  None:
            # TODO: raise credentials exception.
            raise Exception("User not found.")
        
        return ent.to_model()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> str:
        """TODO: Add documentation here."""
        try:
            return self._pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            raise Exception("Found it!" + str(e))
    
    def get_password_hash(self, password: str) -> str:
        """TODO: Add documentation here."""
        return self._pwd_context.hash(password)

    def get_current_user(self, token: str) -> User:
        """TODO: Add documentation here."""

        payload = jwt.decode(token=token, key=self._SECRET_KEY, algorithms=self._ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            # TODO: Create a custom credentials exception here.
            raise Exception("Credentials Exception")
        
        user = self.get_user(username=username)
        return user
    
    def get_current_active_user(self, token: str):
        """TODO: Add documentation here."""
        current_user = self.get_current_user(token)

        if current_user.disabled:
            # TODO: Raise custom exception here.
            raise Exception("User is disabled.")
            
        return current_user
    
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """TODO: Add documentation here."""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._SECRET_KEY, algorithm=self._ALGORITHM)

        return encoded_jwt
    
    def login(self, username: str, plain_password: str) -> Dict[str, str]:
        """TODO: Add documentation here"""
        # Find user with the given username.
        query = select(UserEntity).where(UserEntity.username == username)
        user_entity = self._session.scalar(query)

        if not user_entity:
            # TODO: Raise custom exception here.
            raise Exception("User not found")
        
        if not self.verify_password(plain_password=plain_password, hashed_password=user_entity.hashed_password):
            #TODO: Raise custom exception here.
            raise Exception("Incorrect username or password.")
        
        access_token_expires = timedelta(minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
    
    


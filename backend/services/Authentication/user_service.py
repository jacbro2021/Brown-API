"""Service layer for the user module."""

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session
from jose import jwt, ExpiredSignatureError, JWTError
from passlib.context import CryptContext

from ...env import getenv
from ...database import db_session
from ...models.Authentication.user import User
from ...entities.Authentication.user_entity import UserEntity
from .exceptions import UserNotFoundException, InvalidTokenException, DisabledUserException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

SECRET_KEY = getenv("JWT_SECRET")
ALGORITHM = getenv("ALGORITHM")
ACCESSS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

class UserService():
    """
    Service that will make any API route protected and can be used to retrieve the 
    current user.
       
    To add authentication protection to a route, add a dependency for this service.
    The route will then be unusable unless the caller passes an 'Authorization' header
    with a value of 'Bearer xxx' where xxx represents a valid JWT token.
    """
    _session: Session
    _token: str
    _pwd_context: CryptContext

    def __init__(self,
                session = Depends(db_session),
                token = Depends(oauth2_scheme)
    ):
        self._session = session
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self._token = token

    def _get_user(self, username: str) -> User:
        """
        Helper method that retrieves the user with the matching username from the database.
        
        Args:
            username: The username for the user to search for.
            
        Returns:
            User: The user which has a username matching the username Arg.
            
        Raises:
            UserNotFoundException: If there is no user in the database with a matching username.
        """

        query = select(UserEntity).where(UserEntity.username == username)
        ent: UserEntity | None = self._session.scalar(query)

        if ent ==  None:
            raise UserNotFoundException()
        
        return ent.to_model()

    def _get_current_user(self, token: str) -> User:
        """
        Helper method that decodes a JWT token and retrieves a user.
        
        Args:
            token: The token to decode and use to find the user.
            
        Returns:
            User: The user decoded from the token.
            
        Raises:
            DisabledUserException: If the token payload is expired.
            InvalidTokenException: If the token payload is improperly formatted.
            UserNotFoundException: If there is no user in the database with a matching username.
        """

        # decode the JWT into a dictionary.
        try:
            payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        except ExpiredSignatureError as e:
            raise DisabledUserException()
        except JWTError as e:
            raise InvalidTokenException()

        # Check that the subject exists in the dictionary.
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenException()
        
        # Retrieve and return the User object.
        user = self._get_user(username=username)
        return user
    
    def get_current_active_user(self) -> User:
        """
        Gets a current user and validates that the user is not disabled (non-expired JWT).
        
        Returns:
            User: The current active user.

        Raises:
            InvalidTokenException: If the token payload is improperly formatted.
            UserNotFoundException: If there is no user in the database with a matching username.
            DisabledUserException: If the current user is disabled in the database.
        """

        current_user = self._get_current_user(self._token)
        if current_user.disabled:
            raise DisabledUserException()
            
        return current_user
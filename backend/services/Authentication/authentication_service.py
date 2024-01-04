"""Service to manage the creation the authentication process for users."""

from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends
from passlib.context import CryptContext
from email_validator import validate_email, EmailNotValidError

from .exceptions import UserNotFoundException, InvalidCredentialsException
from ...entities.Authentication.user_entity import UserEntity
from ...models.Authentication.user import User, NewUser
from ...models.Authentication.token import Token
from ...database import db_session
from ...env import getenv

SECRET_KEY = getenv("JWT_SECRET")
ALGORITHM = getenv("ALGORITHM")
ACCESSS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class AuthenticationService():
    """Class to perform all actions pertaining to logins."""

    _session: Session
    _pwd_context: CryptContext

    def __init__(self, session: Session = Depends(db_session)):
        self._session = session
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Helper method to verify that a plain text password matches a hashed password.
        
        Args:
            plain_password: A plain text password input by the user.
            hashed_password: A hashed password retrieved from the database.
            
        Returns:
            bool: True if the passwords match, false otherwise.
        """
        return self._pwd_context.verify(plain_password, hashed_password)

    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """
        Helper method that creates a JWT token using a given dictionary and expires delta.
        
        Args:
            data: dictionary, ideally holding a key value pair for the key 'sub' and value of the users username.
            expires_delta: Timedelta indicating how long the key should be valid for.
            
        Returns:
            str: then encoded JWT.
        """
        
        # Create a copy of the input dictionary
        to_encode = data.copy()

        # Create the expiry date.
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        
        # Add the expiry date to the dictionary and create the JWT.
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encoded_jwt
        
    def login(self, username: str, plain_password: str) -> Token:
        """
        Logs in a user with the matching username and password.
        
        Args:
            username: The username of the user to be logged in.
            plain_password: The plain text pssword of the user to be logged in.
            
        Returns:
            Dict[str, str]: Dictionary with a key value pair for 'access token' and for 'token_type'.

        Raises:
            UserNotFoundException: If a user with a matching username is not found in the database.
            InvalidCredentialsException: If the password or username are invalid for a user. 
        """

        # Find user with the given username.
        query = select(UserEntity).where(UserEntity.username == username)
        user_entity = self._session.scalar(query)

        if not user_entity:
            raise UserNotFoundException()
        
        # Verify the password input by the user.
        if not self._verify_password(plain_password=plain_password, hashed_password=user_entity.hashed_password):
            raise InvalidCredentialsException()
        
        # Create and return the access token.
        access_token_expires = timedelta(minutes=ACCESSS_TOKEN_EXPIRE_MINUTES)
        access_token = self._create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="Bearer")
    
    def _get_password_hash(self, password: str) -> str:
        """
        Helper method that creates a hashed version of a plain text password.
        
        Args:
            password: The plain text password to be hashed.
            
        Returns:
            str: The hashed password.
        """
        return self._pwd_context.hash(password)
    
    def _create_refresh_token(self, user: User) -> User:
        """
        Create a refresh token to be assigned to a user during account creation.
        
        Args:
            user: the user that is being created.
            
        Returns:
            User: the updated user with a valid refresh_token_string.
        """

        refresh_token_string = f"{user.username}{user.email}{user.hashed_password}"
        user.refresh_token = self._pwd_context.hash(refresh_token_string)

        return user
    
    def _validate_unique_user(self, username: str, hashed_password: str, email: str) -> bool:
        """TODO: Add documentation here."""
        query = select(UserEntity).where(UserEntity.username == username)
        ent: UserEntity | None = self._session.scalar(query)
        if ent:
            return False
        
        query = select(UserEntity).where(UserEntity.email == email)
        ent: UserEntity | None = self._session.scalar(query)
        if ent:
            return False
        
        query = select(UserEntity).where(UserEntity.hashed_password == hashed_password)
        ent: UserEntity | None = self._session.scalar(query)
        if ent:
            return False
        
        return True

    
    def create_user(self, username: str, password: str, email: str, full_name: str):
        
        if username == "" or password == "" or email == "" or full_name == "":
            # TODO: Create custom exception
            raise Exception("Blank fields")
        
        if username.replace(" ", "") != username:
            # TODO: Create custom exception
            raise Exception("Whitespace in username")
        elif password.replace(" ", "") != password:
            # TODO: Create custom exception
            raise Exception("Whitespace in password")
        
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError as e:
            # TODO: Create custom exception
            raise Exception("Invalid email")
        
        hashed_password = self._get_password_hash(password=password)

        if not self._validate_unique_user(username=username, hashed_password=hashed_password, email=email):
            # TODO: Create a custom exception.
            raise Exception("non unique user")

        new_user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name
        )

        new_user = self._create_refresh_token(user=new_user)

        new_user_entity = UserEntity.from_model(new_user)
        try: 
            self._session.add(new_user_entity)
        except:
            print("error occured here.")
        
        self._session.commit()

        token: Token = self.login(username=username, plain_password=password)

        return NewUser(email=new_user.email,
                       username=new_user.username, 
                       full_name=new_user.full_name, 
                       refresh_token=new_user.refresh_token, 
                       access_token=token.access_token)
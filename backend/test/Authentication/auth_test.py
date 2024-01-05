"""Tests for the authentication module."""

import pytest
from sqlalchemy.orm import Session

from ...services.Authentication.user_service import UserService
from ...services.Authentication.authentication_service import AuthenticationService
from ...services.Authentication.exceptions import (UserNotFoundException,
                                                    DisabledUserException,
                                                    InvalidCredentialsException, 
                                                    InvalidTokenException,
                                                    InvalidUserInputPropertyException,
                                                    DuplicateUserException
                                                  )
from ...models.Authentication.user import NewUser
from ...models.Authentication.token import Token

@pytest.fixture(autouse=True)
def user_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.
    It constructs a new, empty UserService object."""
    user_service: UserService = UserService(session=session)
    return user_service

@pytest.fixture(autouse=True)
def auth_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.
    It constructs a new, empty AuthenticationService object."""
    auth_service: AuthenticationService = AuthenticationService(session=session)
    return auth_service

def test_create_user(auth_service: AuthenticationService, user_service: UserService):
    """Tests create user basic usage."""
    user: NewUser = auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")
    assert user 
    ent = user_service._get_user(username=user.username)
    assert ent

def test_create_multiple_users(auth_service: AuthenticationService):
    """Tests that multiple users can be created without throwing any exceptions."""
    auth_service.create_user(username="johndeere", password="anothersecret", email="johndeere@gmail.com", full_name="John deere")
    auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")

def test_create_user_blank_property(auth_service: AuthenticationService):
    """Checks that an error is thrown when create user is called with blank properties."""
    try:
        auth_service.create_user(username="", password="", email="", full_name="")
        pytest.fail()
    except InvalidUserInputPropertyException:
        assert True

def test_create_user_invalid_username(auth_service: AuthenticationService):
    """Checks that an exception is raised when a user is created with an invalid email"""
    try:
        auth_service.create_user(username="test", password="test", email="test", full_name="test")
        pytest.fail()
    except InvalidUserInputPropertyException:
        assert True

def test_create_user_space_in_password(auth_service: AuthenticationService):
    """Tests that an exception is raised when a user is created with a space in their username or password."""
    try:
        auth_service.create_user(username="John doe", password="test test", email="normal@gmail.com", full_name="test")
        pytest.fail()
    except InvalidUserInputPropertyException:
        assert True

def test_create_duplicate_user(auth_service: AuthenticationService):
    """Tests that an exception is thrown when a user is created with the same username, email, or password as another user."""
    auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")

    try:
        auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")
        pytest.fail()
    except DuplicateUserException:
        assert True

def test_login_basic_usage(auth_service: AuthenticationService):
    """Tests basic usage for login service method."""
    auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")
    token = auth_service.login(username="johndoe", plain_password="secret")
    assert token
    assert token.access_token

def test_login_multiple_users(auth_service: AuthenticationService):
    """Tests that multiple users can be logged in at once."""
    auth_service.create_user(username="johndeere", password="anothersecret", email="johndeere@gmail.com", full_name="John deere")
    auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")

    token1 = auth_service.login(username="johndeere", plain_password="anothersecret")
    token2 = auth_service.login(username="johndoe", plain_password="secret")

    assert token1
    assert token2
    assert token1.access_token != token2.access_token

def test_login_nonexistent_user(auth_service: AuthenticationService):
    """Tests that an exception is raised when a user is logged in that does not exists."""
    try:
        auth_service.login(username="none", plain_password="none")
        pytest.fail()
    except UserNotFoundException:
        assert True

def test_invalid_credentials(auth_service: AuthenticationService):
    """Tests that an exception is raised when invalid credentials are passed to log a user in."""
    auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")

    try:
        auth_service.login(username="johndoe", plain_password="none")
        pytest.fail()
    except InvalidCredentialsException:
        assert True

def test_refresh_access_token(auth_service: AuthenticationService):
    """Test refresh access token basic usage."""
    new_user: NewUser = auth_service.create_user(username="johndoe", password="secret", email="johndoe@gmail.com", full_name="John Doe")
    assert new_user
    token: Token = auth_service.refresh_access_token(refresh_token=new_user.refresh_token)
    assert token
    assert token.access_token

def test_refresh_access_token_invalid_user(auth_service: AuthenticationService):
    """Test that an exception is raised when a token is refreshed that does not correspond to a user."""
    try:
        auth_service.refresh_access_token(refresh_token="fake")
        pytest.fail()
    except UserNotFoundException:
        assert True
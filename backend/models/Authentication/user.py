"""Pydantic model to represent the 'UserEntity' across application layers."""

from pydantic import BaseModel

class UserBase(BaseModel):
    """Base for the user class containing the pk id for the 'User'."""
    id: int | None = None

class User(UserBase, BaseModel):
    """Pydantic Model to represent the 'UserEntity'."""
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    full_name: str = ""
    refresh_token: str = ""
    disabled: bool = False

class NewUser(BaseModel):
    """Pydantic model to return to the user on successful user creation"""
    email: str = ""
    username: str = ""
    full_name: str = ""
    refresh_token: str = ""
    access_token: str = ""
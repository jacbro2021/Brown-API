"""Pydantic model to represent the 'UserEntity' across application layers."""

from pydantic import BaseModel

class UserBase(BaseModel):
    """Base for the user class containing the pk id for the 'User'."""
    id: int

class User(UserBase, BaseModel):
    """Pydantic Model to represent the 'UserEntity'."""
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    email: str = ""
    full_name: str = ""
    disabled: bool = False
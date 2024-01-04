"""Pydantic model to represent 'Tokens' across application layers."""

from pydantic import BaseModel

class Token(BaseModel):
    """Model to represent the JWT that is used to authenticate users."""
    access_token: str = ""
    token_type: str = ""
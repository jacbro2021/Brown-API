"""Pydantic model to represent 'Tokens' across application layers."""

from pydantic import BaseModel

class Token(BaseModel):
    """Model to represent the 'TokenEntity' that is stored in the database."""
    access_token: str = ""
    token_type: str = ""
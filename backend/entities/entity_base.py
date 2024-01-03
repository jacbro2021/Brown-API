"""Abstract superclass of all entities in the application."""

from sqlalchemy.orm import DeclarativeBase

class EntityBase(DeclarativeBase):
    pass
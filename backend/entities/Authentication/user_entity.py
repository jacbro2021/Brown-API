"""Declaration for the user table in the database."""

from ..entity_base import EntityBase
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from typing import Self
from ...models.Authentication.user import User

class UserEntity(EntityBase):
    """Entity to represent Users and define the columns for the user table in the database."""

    __tablename__ = "user"

    # Primary key to track each user.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # The email for the user.
    email: Mapped[str] = mapped_column(String, nullable=False)
    # The username for the user.
    username: Mapped[str] = mapped_column(String, nullable=False)
    # The hashed password of the user.
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    # The full name of the user.
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    # Boolean flag to represent if the token for the user is valid.
    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False)

    @classmethod
    def from_model(cls, user: User) -> Self:
        """
        Convert a user model to a user entity.
        
        Args: 
            user: The user model to be converted.
            
        Returns:
            Self: The newly created user entity.
        """
        
        return cls(
            id = user.id,
            username = user.username,
            hashed_password = user.hashed_password,
            full_name = user.full_name,
            disabled = user.disabled,
        )
    

    def to_model(self) -> User:
        """
        Convert self to a user model instance.
        
        Returns:
            User: The model representation of self.
        """

        return User(
            id=self.id,
            username=self.username,
            hashed_password=self.hashed_password,
            full_name=self.full_name,
            disabled=self.disabled,
        )
    
    def update(self, user: User) -> None:
        """
        Update a user entity using a provided model.
        
        Args:
            user: The user model to update the entity with.
        """

        self.username = user.username
        self.hashed_password = user.hashed_password
        self.full_name = user.full_name
        self.disabled = user.disabled
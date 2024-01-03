"""Reset Database and add some test data."""

from ..entities.entity_base import  EntityBase
from ..entities.Authentication.user_entity import UserEntity
from ..database import engine

from sqlalchemy.orm import Session
from ..models.Authentication.user import User
import sqlalchemy
from ..env import getenv

EntityBase.metadata.drop_all(engine)
EntityBase.metadata.create_all(engine)

def _engine_str(database=getenv("POSTGRES_DATABASE")) -> str:
    """Helper function for reading settings from environment variables to produce connection string."""
    dialect = "postgresql+psycopg2"
    user = getenv("POSTGRES_USER")
    password = getenv("POSTGRES_PASSWORD")
    host = getenv("POSTGRES_HOST")
    port = getenv("POSTGRES_PORT")
    return f"{dialect}://{user}:{password}@{host}:{port}/{database}"

engine = sqlalchemy.create_engine(_engine_str(), echo=True)
"""Application-level SQLAlchemy database engine."""

session: Session = Session(engine)

mod: User = User(
    id=0,
    email="johndoe@example.com",
    username="johndoe",
    hashed_password="fakehashsecret",
    full_name="John Doe",
    disabled=False
)

ent = UserEntity.from_model(mod)

session.add(ent)
session.commit()

session.close()

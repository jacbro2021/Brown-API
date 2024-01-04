"""Reset Database and add some test data."""

from ..entities.entity_base import  EntityBase
from ..entities.Authentication.user_entity import UserEntity
from ..database import engine

from sqlalchemy.orm import Session
from ..models.Authentication.user import User
import sqlalchemy
from ..env import getenv
from ..services.Authentication.authentication_service import AuthenticationService

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

service = AuthenticationService(session=session)

mod: User = User(
    id=0,
    email="johndoe@example.com",
    username="johndoe",
    hashed_password=f"{service.get_password_hash(password='secret')}",
    full_name="John Doe",
    disabled=False
)

mod2: User = User(
    id=1,
    email="johngreen@example.com",
    username="johngreen",
    hashed_password="fakehashsecret2",
    full_name="John Green",
    disabled=True
)

ent = UserEntity.from_model(mod)
ent2 = UserEntity.from_model(mod2)

session.add(ent)
session.add(ent2)
session.commit()

session.close()

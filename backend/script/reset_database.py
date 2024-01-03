"""Reset Database"""

from ..entities.entity_base import  EntityBase
from ..entities.Authentication.user_entity import UserEntity
from ..database import engine

EntityBase.metadata.drop_all(engine)
EntityBase.metadata.create_all(engine)
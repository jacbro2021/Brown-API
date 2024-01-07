"""Test data for the 'plant_test' tests for the plant service."""

from sqlalchemy.orm import Session
from ..reset_table_id_seq import reset_table_id_seq

from ...models.Authentication.user import User
from ...entities.Authentication.user_entity import UserEntity
from ...models.Folium.plant import Plant
from ...entities.Folium.plant_entity import PlantEntity

user1 = User(
    id=0,
    email="johndoe@gmail.com",
    username="johndoe",
    hashed_password="secret",
    full_name="john doe",
    refresh_token="tok",
    disabled=False
)

user2 = User(
    id=1,
    email="johndeer@gmail.com",
    username="johndeere",
    hashed_password="secret2",
    full_name="john deere",
    refresh_token="tok2",
    disabled=False
)

plant1 = Plant(
    id=0,
    common_name="test1",
    scientific_name="fake",
    type="fake",
    cycle="fake",
    watering="fake",
    watering_period="fake",
    watering_benchmark_unit="fake",
    watering_benchmark_value="fake",
    sunlight="fake",
    pet_poison=False,
    human_poison=True,
    description="fake",
    image_url="fake",
    owner_username="johndoe",
    last_watering="fake",
    health_history=list(),
)

plant2 = Plant(
    id=1,
    common_name="test2",
    scientific_name="fake",
    type="fake",
    cycle="fake",
    watering="fake",
    watering_period="fake",
    watering_benchmark_unit="fake",
    watering_benchmark_value="fake",
    sunlight="fake",
    pet_poison=False,
    human_poison=True,
    description="fake",
    image_url="fake",
    owner_username="johndeere",
    last_watering="fake",
    health_history=list(),
)

users = [user1, user2]

plants = [plant1, plant2]

def insert_test_data(session: Session):
    """Insert fake data for testing."""
    
    # Add users to db.
    for user in users:
        new_user = UserEntity.from_model(user=user)
        session.add(new_user)

    # Add plants to db.
    for plant in plants:
        new_plant = PlantEntity.from_model(plant=plant)
        session.add(new_plant)

    ent = session.query(UserEntity).all()

    reset_table_id_seq(session=session, entity=UserEntity, entity_id_column=UserEntity.id, next_id=len(users) + 1)
    reset_table_id_seq(session=session, entity=PlantEntity, entity_id_column=PlantEntity.id, next_id=len(plants) + 1)


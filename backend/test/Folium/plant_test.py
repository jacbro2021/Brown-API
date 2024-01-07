"""Tests for the folium plant module."""

"""Unit tests for the plant service"""

import pytest
from sqlalchemy.orm import Session
from .plant_test_data import insert_test_data

from ...services.Folium.exceptions import PlantNotFoundException, PlantBlankIdException, PlantOwnerUsernameInvalidException

from ...services.Folium.plant_service import PlantService
from ...models.Folium.plant import Plant

@pytest.fixture(autouse=True, scope="function")
def plant_service(session: Session):
    """This PyTest fixture is injected into each test parameter of the same name below.
    It constructs a new, empty PlantService object."""
    insert_test_data(session)
    session.commit()
    plant_service = PlantService(session=session)
    return plant_service

def test_get_all_user_plants(plant_service: PlantService):
    """Test basic usage for get all user plants service method"""

    plants = plant_service.get_all_user_plants("johndoe")
    assert len(plants) == 1
    assert plants[0].common_name == "test1"


def test_get_all_user_plants_correct_plants(plant_service: PlantService):
    """Test that get all user plants service method returns the correct plants"""

    plants = plant_service.get_all_user_plants("johndoe")
    assert len(plants) == 1
    assert plants[0].common_name != "test2"

def test_create_plant(plant_service: PlantService):
    """Tests create plant service method basic usage."""

    plant = Plant(
        common_name="fake",
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
        health_history=[],
    )
    plant_service.create_plant(plant=plant, owner_username="johndeere")
    assert len(plant_service.get_all_user_plants("johndeere")) == 2

def test_create_plant_other_user(plant_service: PlantService):
    """Tests that a user cannot create a plant for another user."""
    plant = Plant(
        common_name="fake",
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
        health_history=[],
    )
    try:
        plant_service.create_plant(plant=plant, owner_username="johndoe")
        pytest.fail()
    except PlantOwnerUsernameInvalidException:
        assert True


def test_remove_plant(plant_service: PlantService):
    """Tests basic functionality of remove plant service method."""

    plant = Plant(owner_username="johndoe")
    plant = plant_service.create_plant(plant=plant, owner_username="johndoe")
    assert len(plant_service.get_all_user_plants("johndoe")) == 2
    plant_service.remove_plant(plant=plant, owner_username="johndoe")
    assert len(plant_service.get_all_user_plants("johndoe")) == 1

def test_remove_other_user_plant(plant_service: PlantService):
    """Tests that a user cannot remove another users plants."""

    plant = Plant(id=0, owner_username="johndoe")
    try:
        plant_service.remove_plant(plant=plant, owner_username="johndeere")
        pytest.fail()
    except PlantOwnerUsernameInvalidException:
        assert True

def test_remove_nonexistent_plant(plant_service: PlantService):
    """Tests that an error is thrown when remove plant is called on a plant that is not in the db."""
    
    plant = Plant(id=3, owner_username="johndoe")
    try:
        plant_service.remove_plant(plant=plant, owner_username="johndoe")
        pytest.fail()
    except PlantNotFoundException:
        assert True

def test_remove_plant_blank_id(plant_service: PlantService):
    """Tests that an exception is raised when a plant is removed with a blank id"""
    plant = Plant(owner_username="johndoe")
    try:
        plant_service.remove_plant(plant=plant, owner_username="johndoe")
        pytest.fail()
    except PlantBlankIdException:
        assert True

def test_update_plant(plant_service: PlantService):
    """Test basic usage of update plant service method."""

    plant = Plant(id=0, common_name="not fake", owner_username="johndoe")
    plant = plant_service.create_plant(plant=plant, owner_username="johndoe")
    plant.common_name = "super fake"
    updated_plant = plant_service.update_Plant(plant=plant, owner_username="johndoe")
    assert updated_plant.common_name == "super fake"

def test_update_plant_nonexistent_plant(plant_service: PlantService):
    """Test that an exception is raised when a plant is updated that does not exist for an owner"""

    plant = Plant(id=0, owner_key="user2")

    try:
        plant_service.update_Plant(plant=plant)
        pytest.fail()
    except:
        assert True
"""Plant service used by the plant api to perform actions on the plant table in the db."""

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from ...database import db_session

from ...models.Folium.plant import Plant
from ...entities.Folium.plant_entity import PlantEntity
from .exceptions import PlantBlankIdException, PlantNotFoundException, PlantOwnerUsernameInvalidException

class PlantService:
    """Plant service to perform actions on the plant table."""

    def __init__(self,
                 session: Session = Depends(db_session)):
        self._session = session
        
    def __find_plant_entity(self, plant_id: int, owner_username: str) -> PlantEntity:
        """
        Helper method that either retrieves a plant from the database or raises an exception.
        
        Args:
            plant_id: The id of the plant to search for.
            owner_username: The key of the owner that owns the plant to search for.

        Returns:
            PlantEntity: The Entity representation of the retrieved plant.
        
        Raises:
            PlantBlankIdException: If the plants ID is blank.
            PlantNotFoundException: If the plant is not found in the database.
        """

        # If plant_id is empty, raise exception
        if not plant_id:
            raise PlantBlankIdException()

        # Query the database to find the plant to be deleted.
        query = select(PlantEntity).where(PlantEntity.id == plant_id)
        plant_entity: PlantEntity | None = self._session.scalar(query)

        # If not plant found, raise error. 
        if plant_entity == None or plant_entity.owner_username != owner_username:
            raise PlantNotFoundException()
        else:
            return plant_entity

    def get_all_user_plants(self, owner_username: str) -> list[Plant]:
        """
        Retrieve all plants for a given user from the database.
        
        Args:
            key: The key for the user.
            
        Returns:
            list[Plant]: The list of the users plant objects.
        """

        # Create list of plants and query db to retrieve entities.
        plants: list[Plant] = []
        plant_entities = self._session.query(PlantEntity).where(PlantEntity.owner_username == owner_username)

        # Loop through retrieved entities and convert to plant models.
        for entity in plant_entities:
            plant = entity.to_model()
            plants.append(plant)

        # Return the list of plants for the user with the provided key.
        return plants

    def create_plant(self, plant: Plant, owner_username: str) -> Plant:
        """
        Add a new plant to the database.
        
        Args:
            plant: The plant to add to the database.
            
        Returns:
            Plant: the plant that was successfully added to the database.

        raises: 
            PlantOwnerUsernameInvalidException: If the plants 'ownerusername' does not match that of the caller.
        """
        if plant.owner_username != owner_username:
            raise PlantOwnerUsernameInvalidException()
        
        plant.id = None
        plant_entity = PlantEntity.from_model(plant=plant)
        self._session.add(plant_entity)
        self._session.commit()

        return plant_entity.to_model()

    def remove_plant(self, plant: Plant, owner_username: str) -> Plant:
        """
        Removes a plant from the database.
        
        Args: 
            plant: The plant to remove from the database.
            
        Returns:
            Plant: The plant that was successfully removed from the database.

        Raises:
            PlantNotFoundException: If the plant with the given id is not found in the database.
            PlantBlankIdException: If the plants ID is blank.
            PlantOwnerUsernameInvalidException: If the plants 'ownerusername' does not match that of the caller.
        """
        if plant.owner_username != owner_username:
            raise PlantOwnerUsernameInvalidException()
        
        # Query the database to find the plant to be deleted.
        plant_entity = self.__find_plant_entity(plant_id=plant.id, owner_username=plant.owner_username)
        
        # Delete plant from database and return. 
        self._session.delete(plant_entity)
        self._session.commit()

        return plant_entity.to_model()

    def update_Plant(self, plant: Plant, owner_username: str) -> Plant:
        """
        Updates a plant in the database.
        
        Args:
            plant: The updated version of the plant.
            
        Returns:
            Plant: The model representation of the plant that was updated in the database.

        Raises:
            PlantNotFoundException: If the plant with the given id is not found in the database.
            PlantBlankIdException: If the plants ID is blank.
            PlantOwnerUsernameInvalidException: If the plants 'ownerusername' does not match that of the caller.
        """
        if plant.owner_username != owner_username:
            raise PlantOwnerUsernameInvalidException()

        # Query the database to find the plant to be deleted.
        plant_entity = self.__find_plant_entity(plant_id=plant.id, owner_username=plant.owner_username)
        
        # Update the plant entity and commit the changes.
        plant_entity.update(plant=plant)
        self._session.commit()

        return plant_entity.to_model()

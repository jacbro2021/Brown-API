"""API routes for the Folium plant module."""

from fastapi import Depends, HTTPException, APIRouter

from ...services.Folium.plant_service import PlantService
from ...services.Authentication.user_service import UserService
from ...models.Folium.plant import Plant
from ...services.Folium.exceptions import PlantOwnerUsernameInvalidException, PlantNotFoundException, PlantBlankIdException

api = APIRouter(prefix="/folium/plant")
openapi_tags = {
    "name":"Folium Plant",
    "description":"Routes to interact with Folium API plant functionality."   
}

@api.get("/get_user_plants", tags=["Folium Plant"])
def get_user_plants(plant_service: PlantService = Depends(),
                    user_service: UserService = Depends(),) -> list[Plant]:
    """
    Get all of the plants that belong to a user.
    
    Args:
        key: The key of the user to retrieve plants for.
        
    Returns:
        list[Plant]: A list of the plants that belong to the user.

    Raises:
        401: If the user is not authorized or the access token is improperly formatted.
    """

    try:
        return plant_service.get_all_user_plants(owner_username=user_service.get_current_active_user().username)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@api.post("/create_plant", tags=["Folium Plant"])
def create_plant(plant: Plant,
                 plant_service: PlantService = Depends(),
                 user_service: UserService = Depends()) -> Plant:
    """
    Create a new plant for a user in the database.
    
    Args:
        plant: The plant object to be added to the database.
        
    Returns:
        Plant: The newly created plant object.
        
    Raises:
        422: If the input key is an empty string.
        401: If the user is not authorized or the access token is improperly formatted.
    """

    try:
        return plant_service.create_plant(plant=plant, owner_username=user_service.get_current_active_user().username)
    except PlantOwnerUsernameInvalidException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@api.put(path="/update_plant", tags=["Folium Plant"])
def update_plant(plant: Plant,
                 plant_service: PlantService = Depends(),
                 user_service: UserService = Depends()) -> Plant:
    """
    Updates and returns a plant that is already in the database.

    Args:
        plant: The plant to update in the database.
        
    Returns:
        Plant: The updated plant.
        
    Raises:
        404: If the key does not match a user in the database or the plant is not found in the database.
        422: If the input key or plant id is an empty string.
        401: If the user is not authorized or the access token is improperly formatted.
    """

    try:
        return plant_service.update_Plant(plant=plant, owner_username=user_service.get_current_active_user().username)
    except PlantNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlantBlankIdException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@api.delete(path="/delete_plant", tags=["Folium Plant"])
def delete_plant(plant: Plant,
                 plant_service: PlantService = Depends(),
                 user_service: UserService = Depends()) -> Plant:
    """
    Removes a plant from the database.
    
    Args:
        plant: The plant to delete from the database.
        
    Returns:
        Plant: The plant that was successfully deleted from the database.

    Raises:
        404: If the plant passed as an arg is not found in the database.
        422: If the plant.owner_username does not match that of the currently authenticated user.
        401: If the user is not authorized or the access token is improperly formatted.
    """

    try:
        return plant_service.remove_plant(plant=plant, owner_username=user_service.get_current_active_user().username)
    except PlantNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PlantBlankIdException as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
"""Exceptions for the Folium module"""

class PlantNotFoundException(Exception):
    """Exception to be thrown when the database is queried for a plant that does not exist."""
    def __init__(self):
        super().__init__(
            f"Plant not found."
        )

class PlantBlankIdException(Exception):
    """Exception to be thrown when an empty Id is passed to be checked in the database."""
    def __init__(self):
        super().__init__(
            "Empty ID passed. Plant ID field must be populated."
        )

class PlantOwnerUsernameInvalidException(Exception):
    """Exception to be thrown when a plant is created that does not have the 'owner_username' of the calling user."""
    def __init__(self):
        super().__init__(
            "Plant property 'owner_username' must match that of the authenticated user."
        )
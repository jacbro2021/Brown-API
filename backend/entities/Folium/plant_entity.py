"""Declaration for the plant table in the database."""

from sqlalchemy import Integer, String, ARRAY, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from typing import Self

from ..entity_base import EntityBase
from ...models.Folium.plant import Plant

class PlantEntity(EntityBase):
    """Entity to represent plants that are persisted in the database."""
 # The name of the table in the database.
    __tablename__ = "plant"
    
    # Id of the plant.
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Common name for the plant.
    common_name: Mapped[str] = mapped_column(String)
    # Scientific name for the plant.
    scientific_name: Mapped[str] = mapped_column(String)
    # Type of plant.
    type: Mapped[str] = mapped_column(String)
    # The plants cycle.
    cycle: Mapped[str] = mapped_column(String)
    # The frequency that that the plant should be watered.
    watering: Mapped[str] = mapped_column(String)
    # The time of day that the plant should be watered.
    watering_period: Mapped[str] = mapped_column(String)
    # The amount of time that should pass between the plant being watered.
    watering_benchmark_value: Mapped[str] = mapped_column(String)
    # The unit for the watering benchmark value.
    watering_benchmark_unit: Mapped[str] = mapped_column(String)
    # The amount of sunlight that the plant should get.
    sunlight: Mapped[str] = mapped_column(String)
    # true/false poisonous to pets.
    pet_poison: Mapped[bool] = mapped_column(Boolean)
    # True/false poisonous to humans.
    human_poison: Mapped[bool] = mapped_column(Boolean)
    # Description of the plant.
    description: Mapped[str] = mapped_column(String)
    # Url for an image of the plant.
    image_url: Mapped[str] = mapped_column(String)
    # The key for the owner of the plant.
    owner_username: Mapped[str] = mapped_column(String, nullable=False)
    # Date last watered.
    last_watering: Mapped[str] = mapped_column(String)
    # Health history, where each index is a ranking of the plants health from 1-10.
    health_history: Mapped[list[int]] = mapped_column(ARRAY(Integer))

    @classmethod
    def from_model(cls, plant: Plant) -> Self:
        """
        Convert Plant model to Plant entity
        
        Args: 
            plant: plant model
            
        Returns:
            self
        """
        
        return cls(
            id = plant.id,
            common_name = plant.common_name,
            scientific_name = plant.scientific_name,
            type = plant.type,
            cycle = plant.cycle,
            watering = plant.watering,
            watering_period = plant.watering_period,
            watering_benchmark_unit = plant.watering_benchmark_unit,
            watering_benchmark_value = plant.watering_benchmark_value,
            sunlight = plant.sunlight,
            pet_poison = plant.pet_poison,
            human_poison = plant.human_poison,
            description = plant.description,
            image_url = plant.image_url,
            owner_username = plant.owner_username,
            last_watering = plant.last_watering,
            health_history = plant.health_history,
        )
    
    def to_model(self) -> Plant:
        """
        Convert plant entity to plant model.
            
        Returns:
            Plant: model representation of self.
        """

        return Plant(
            id = self.id,
            common_name = self.common_name,
            scientific_name = self.scientific_name,
            type = self.type,
            cycle = self.cycle,
            watering = self.watering,
            watering_period = self.watering_period,
            watering_benchmark_unit = self.watering_benchmark_unit,
            watering_benchmark_value = self.watering_benchmark_value,
            sunlight = self.sunlight,
            pet_poison = self.pet_poison,
            human_poison = self.human_poison,
            description = self.description,
            image_url = self.image_url,
            owner_username = self.owner_username,
            last_watering = self.last_watering,
            health_history = self.health_history,
        )
    
    def update(self, plant: Plant) -> None:
        """
        Updates self using a provided plant model.
        
        Args:
            plant: the plant model to update with.
        """

        self.common_name = plant.common_name
        self.scientific_name = plant.scientific_name
        self.type = plant.type
        self.cycle = plant.cycle
        self.watering = plant.watering
        self.watering_period = plant.watering_period
        self.watering_benchmark_value = plant.watering_benchmark_value
        self.watering_benchmark_unit = plant.watering_benchmark_unit
        self.sunlight = plant.sunlight
        self.pet_poison = plant.pet_poison
        self.human_poison = plant.human_poison
        self.description = plant.description
        self.image_url = plant.image_url
        self.last_watering = plant.last_watering
        self.health_history = plant.health_history
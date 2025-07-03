from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class Route(BaseModel):
    id: UUID | None = None
    driver_id: UUID
    car_plate_number: str
    departure_location_name: str
    departure_time: datetime
    destination_location_name: str

    model_config = ConfigDict(from_attributes=True)
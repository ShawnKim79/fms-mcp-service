from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class Route(BaseModel):
    id: UUID
    driver_id: UUID
    car_plate_number: str
    departure_location_name: str
    departure_time: datetime
    destination_location_name: str

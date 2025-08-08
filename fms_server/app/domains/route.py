from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from controllers.dto.request_dto import RequestCreateRoute

class Route(BaseModel):
    id: Optional[UUID] = None
    driver_id: Optional[UUID] = None
    car_plate_number: Optional[str] = None
    departure_location_name: Optional[str] = None
    departure_time: Optional[datetime] = None
    destination_location_name: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


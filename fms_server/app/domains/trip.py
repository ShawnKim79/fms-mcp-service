from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

class Trip(BaseModel):
    id: UUID | None = None
    ride_route_id: UUID
    passenger_id: UUID
    pickup_request_location_name: str
    pickup_time: datetime
    is_approved: bool = False

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class trip(BaseModel):
    id: UUID
    ride_route_id: UUID
    passenger_id: UUID
    pickup_request_location_name: str
    pickup_time: datetime
    is_approved: bool = False

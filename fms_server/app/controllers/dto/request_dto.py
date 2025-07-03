from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RequestCreatePassenger(BaseModel):
    name: str
    contact_info: str

    model_config = ConfigDict(from_attributes=True)

class RequestCreateRoute(BaseModel):
    driver_id: UUID
    car_plate_number: str
    departure_location_name: str
    departure_time: datetime
    destination_location_name: str

    model_config = ConfigDict(from_attributes=True)

class RequestCreateTrip(BaseModel):
    ride_route_id: UUID
    passenger_id: UUID
    pickup_request_location_name: str
    pickup_time: datetime

    model_config = ConfigDict(from_attributes=True)
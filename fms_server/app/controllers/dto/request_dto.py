from datetime import datetime
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class RequestCreatePassenger(BaseModel):
    name: str
    contact_info: str

    model_config = ConfigDict(from_attributes=True)

class RequestRoute(BaseModel):
    driver_id: UUID
    car_plate_number: str
    departure_location_name: str
    departure_time: datetime
    destination_location_name: str

    # TODO: 추후 제거
    driver_name: str
    driver_contact_info: str
    passenger_name: str
    passenger_contact_info: str
    confirm_onboard: bool


    model_config = ConfigDict(from_attributes=True)


class RequestCreatePassengerRoute(BaseModel):
    # driver_id: UUID
    # car_plate_number: str
    departure_location_name: str
    departure_time: datetime
    destination_location_name: str

    # TODO: 추후 제거
    # driver_name: str
    # driver_contact_info: str
    passenger_name: str
    passenger_contact_info: str


    model_config = ConfigDict(from_attributes=True)

class RequestInvolveDriverToRoute(BaseModel):
    driver_id: UUID
    car_plate_number: str
    driver_name: str
    driver_contact_info: str


    model_config = ConfigDict(from_attributes=True)


class RequestCreateTrip(BaseModel):
    ride_route_id: UUID
    passenger_id: UUID
    pickup_request_location_name: str
    pickup_time: datetime

    model_config = ConfigDict(from_attributes=True)
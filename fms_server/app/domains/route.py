from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

from controllers.dto.request_dto import RequestRoute, RequestCreatePassengerRoute, RequestInvolveDriverToRoute

class Route(BaseModel):
    id: UUID | None = None
    driver_id: Optional[UUID] = None
    car_plate_number: Optional[str] = None
    departure_location_name: Optional[str] = None
    departure_time: Optional[datetime] = None
    destination_location_name: Optional[str] = None
    driver_name: Optional[str] = None
    driver_contact_info: Optional[str] = None
    passenger_name: Optional[str] = None
    passenger_contact_info: Optional[str] = None
    confirm_onboard: Optional[bool] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PassengerRoute(RequestCreatePassengerRoute):
    id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)

class InvolveDriverToRoute(RequestInvolveDriverToRoute):
    id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)
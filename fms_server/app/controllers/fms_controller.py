from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from pydantic import model_validator
from sqlalchemy.orm import Session

from config.database import get_db_session
from domains.passenger import Passenger
from domains.route import PassengerRoute, Route
from domains.trip import Trip
from controllers.dto.request_dto import RequestCreatePassenger, RequestRoute, RequestCreateTrip, RequestInvolveDriverToRoute, RequestCreatePassengerRoute
from services.fms_service import FmsService


router = APIRouter(prefix="/fms")

def get_fms_service(db_session: Session = Depends(get_db_session)):
    return FmsService(session=db_session)

@router.post("/passengers",  status_code=201)
async def create_passenger(request_passenger: RequestCreatePassenger, fms_service: FmsService = Depends(get_fms_service)):
    print(request_passenger)
    passenger_data: Passenger = Passenger.model_validate(request_passenger)

    return fms_service.create_passenger(passenger_data)

@router.get("/passengers/{passenger_id}", status_code=200)
async def get_passenger(passeger_id:str, fms_service:FmsService = Depends(get_fms_service)):
    passenger_data: Passenger = fms_service.find_passenger(passenger_id=passeger_id)
    return passenger_data


@router.get("/ride_routes", status_code=200)
async def find_ride_routes(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    departure_location_name: Optional[str] = Query(None),
    destination_location_name: Optional[str] = Query(None),
    fms_service: FmsService = Depends(get_fms_service)
):
    return fms_service.find_ride_routes(
        start_time=start_time,
        end_time=end_time,
        departure_location_name=departure_location_name,
        destination_location_name=destination_location_name,
    )


@router.post("/ride_routes/passenger_route", response_model=Route, status_code=200)
async def create_passenger_route(request_passenger_route: RequestCreatePassengerRoute, fms_service: FmsService = Depends(get_fms_service)):
    route_data: PassengerRoute = PassengerRoute.model_validate(request_passenger_route)
    route_data.id = uuid4()
    return fms_service.create_passenger_route(route_data)


@router.put("/ride_routes/{route_id}/involve_driver", response_model=Route, status_code=200)
async def involve_driver_to_route(route_id: UUID, request_involve_driver: RequestInvolveDriverToRoute, fms_service: FmsService = Depends(get_fms_service)):
    updated_route = fms_service.involve_driver_to_route(route_id, request_involve_driver)
    if not updated_route:
        raise HTTPException(status_code=404, detail="Route not found")
    return updated_route


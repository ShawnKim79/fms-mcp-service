from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from pydantic import model_validator
from sqlalchemy.orm import Session

from config.database import get_db_session
from domains.passenger import Passenger
from domains.route import Route
from domains.trip import Trip
from controllers.dto.request_dto import RequestCreatePassenger, RequestCreateRoute, RequestCreateTrip
from services.fms_service import FmsService


router = APIRouter(prefix="/fms")

def get_fms_service(db_session: Session = Depends(get_db_session)):
    return FmsService(session=db_session)

@router.post("/passengers", response_model=Passenger, status_code=201)
async def create_passenger(request_passenger: RequestCreatePassenger, fms_service: FmsService = Depends(get_fms_service)):
    passenger_data: Passenger = Passenger.model_validate(request_passenger)
    passenger_data.id = uuid4()

    return fms_service.create_passenger(passenger_data)

@router.post("/ride_routes", response_model=Route, status_code=201)
async def create_ride_route(request_route: RequestCreateRoute, fms_service: FmsService = Depends(get_fms_service)):
    route_data: Route = Route.model_validate(request_route)
    route_data.id = uuid4()

    return fms_service.create_ride_route(route_data)

@router.get("/ride_routes/{route_id}", response_model=Route, status_code=200)
async def get_ride_route(route_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    route = fms_service.get_ride_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.get("/ride_routes", status_code=200)
async def find_ride_routes(
    driver_id: Optional[UUID] = Query(None),
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    departure_location_name: Optional[str] = Query(None),
    destination_location_name: Optional[str] = Query(None),
    fms_service: FmsService = Depends(get_fms_service)
):
    return fms_service.find_ride_routes(
        driver_id=driver_id,
        start_time=start_time,
        end_time=end_time,
        departure_location_name=departure_location_name,
        destination_location_name=destination_location_name,
    )

@router.put("/ride_routes/{route_id}", response_model=Route, status_code=200)
async def update_ride_route(route_id: UUID, route: Route, fms_service: FmsService = Depends(get_fms_service)):
    updated_route = fms_service.update_ride_route(route_id, route)
    if not updated_route:
        raise HTTPException(status_code=404, detail="Route not found")
    return updated_route

@router.delete("/ride_routes/{route_id}", status_code=204)
async def delete_ride_route(route_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    fms_service.delete_ride_route(route_id)
    return JSONResponse(status_code=204, content=None)

@router.post("/trips", response_model=Trip, status_code=201)
async def create_trip(request_new_trip: RequestCreateTrip, fms_service: FmsService = Depends(get_fms_service)):
    trip_data: Trip = Trip.model_validate(request_new_trip)
    trip_data.id = uuid4()

    return fms_service.create_trip(trip_data)

@router.get("/trips/{request_id}", response_model=Trip, status_code=200)
async def get_trip(request_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    trip = fms_service.get_trip(request_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.get("/trips", status_code=200)
async def find_trips(
    ride_route_id: Optional[UUID] = None,
    passenger_id: Optional[UUID] = None,
    is_approved: Optional[bool] = None,
    fms_service: FmsService = Depends(get_fms_service)
):
    return fms_service.find_trips(
        ride_route_id=ride_route_id,
        passenger_id=passenger_id,
        is_approved=is_approved,
    )

@router.put("/trips/{request_id}/approve", response_model=Trip, status_code=200)
async def approve_trip(request_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    updated_trip = fms_service.approve_trip(request_id)
    if not updated_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return updated_trip

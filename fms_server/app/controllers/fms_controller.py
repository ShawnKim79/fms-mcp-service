from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from uuid import UUID
from datetime import datetime
from typing import Optional
from database import get_db_session
from sqlalchemy.orm import Session

from app.domains.passenger import Passenger
from app.domains.route import Route
from app.domains.trip import trip as RideRequest
from app.services.fms_service import FmsService

router = APIRouter(prefix="/fms")

def get_fms_service(db_session: Session = Depends(get_db_session)):
    return FmsService(session=db_session)

@router.post("/passengers", response_model=Passenger, status_code=201)
async def create_passenger(passenger: Passenger, fms_service: FmsService = Depends(get_fms_service)):
    return await fms_service.create_passenger(passenger)

@router.post("/ride_routes", response_model=Route, status_code=201)
async def create_ride_route(route: Route, fms_service: FmsService = Depends(get_fms_service)):
    return await fms_service.create_ride_route(route)

@router.get("/ride_routes/{route_id}", response_model=Route, status_code=200)
async def get_ride_route(route_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    route = await fms_service.get_ride_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route

@router.get("/ride_routes", status_code=200)
async def find_ride_routes(
    driver_id: Optional[UUID] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    departure_location_name: Optional[str] = None,
    destination_location_name: Optional[str] = None,
    fms_service: FmsService = Depends(get_fms_service)
):
    return await fms_service.find_ride_routes(
        driver_id=driver_id,
        start_time=start_time,
        end_time=end_time,
        departure_location_name=departure_location_name,
        destination_location_name=destination_location_name,
    )

@router.put("/ride_routes/{route_id}", response_model=Route, status_code=200)
async def update_ride_route(route_id: UUID, route: Route, fms_service: FmsService = Depends(get_fms_service)):
    updated_route = await fms_service.update_ride_route(route_id, route)
    if not updated_route:
        raise HTTPException(status_code=404, detail="Route not found")
    return updated_route

@router.delete("/ride_routes/{route_id}", status_code=204)
async def delete_ride_route(route_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    await fms_service.delete_ride_route(route_id)
    return JSONResponse(status_code=204, content=None)

@router.post("/ride_requests", response_model=RideRequest, status_code=201)
async def create_ride_request(ride_request: RideRequest, fms_service: FmsService = Depends(get_fms_service)):
    return await fms_service.create_ride_request(ride_request)

@router.get("/ride_requests/{request_id}", response_model=RideRequest, status_code=200)
async def get_ride_request(request_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    ride_request = await fms_service.get_ride_request(request_id)
    if not ride_request:
        raise HTTPException(status_code=404, detail="Ride request not found")
    return ride_request

@router.get("/ride_requests", status_code=200)
async def find_ride_requests(
    ride_route_id: Optional[UUID] = None,
    passenger_id: Optional[UUID] = None,
    is_approved: Optional[bool] = None,
    fms_service: FmsService = Depends(get_fms_service)
):
    return await fms_service.find_ride_requests(
        ride_route_id=ride_route_id,
        passenger_id=passenger_id,
        is_approved=is_approved,
    )

@router.put("/ride_requests/{request_id}/approve", response_model=RideRequest, status_code=200)
async def approve_ride_request(request_id: UUID, fms_service: FmsService = Depends(get_fms_service)):
    updated_ride_request = await fms_service.approve_ride_request(request_id)
    if not updated_ride_request:
        raise HTTPException(status_code=404, detail="Ride request not found")
    return updated_ride_request

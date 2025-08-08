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
from controllers.dto.request_dto import RequestCreatePassenger 
from services.fms_service import FmsService


router = APIRouter(prefix="/fms/passenger")

def get_fms_service(db_session: Session = Depends(get_db_session)):
    return FmsService(session=db_session)

@router.post("/",  status_code=201)
async def create_passenger(request_passenger: RequestCreatePassenger, fms_service: FmsService = Depends(get_fms_service)):
    print(request_passenger)
    passenger_data: Passenger = Passenger.model_validate(request_passenger)

    return fms_service.create_passenger(passenger_data)

@router.get("/{passenger_id}", status_code=200)
async def get_passenger(passeger_id:str, fms_service:FmsService = Depends(get_fms_service)):
    passenger_data: Passenger = fms_service.find_passenger(passenger_id=passeger_id)
    return passenger_data


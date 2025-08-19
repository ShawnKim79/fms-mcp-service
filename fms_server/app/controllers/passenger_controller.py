from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional
from pydantic import model_validator
from sqlalchemy.orm import Session

from config.database import get_db_session
from domains.passenger import Passenger, ResponsePassenger
from domains.route import Route
from domains.trip import Trip
from controllers.dto.request_dto import RequestCreatePassenger 
from services.fms_service import FmsService
from services.passenger_service import PassengerService
from utils.security import get_token_payload


router = APIRouter(prefix="/fms/passenger")

def get_fms_service(db_session: Session = Depends(get_db_session)):
    return FmsService(session=db_session)

def get_passenger_service(db_session: Session = Depends(get_db_session)):
    return PassengerService(session=db_session)


@router.post("/",  status_code=201)
async def create_passenger(request_passenger: RequestCreatePassenger, 
                           fms_service: FmsService = Depends(get_fms_service)):
    
    passenger_data: Passenger = Passenger.model_validate(request_passenger)

    return fms_service.create_passenger(passenger_data)

@router.get("/my-info", status_code=200)
async def get_passenger(passenger_service:PassengerService = Depends(get_passenger_service), 
                        payload: dict = Depends(get_token_payload)):
    nickname = payload.get("sub")
    passenger_data: Passenger = passenger_service.find_by_nickname(nickname)
    if passenger_data is None:
        raise HTTPException(status_code=404, detail="Passenger not found")
    
    
    return ResponsePassenger.model_validate(passenger_data)


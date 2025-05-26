from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/fms")

@router.post("/route", status_code=201)
def create_route():
    return "create_route"

@router.post("/passenger", status_code=201)
def create_passenger():
    return "create passenger"

@router.post("/trip", status_code=201)
def create_trip():
    return "create trip"

@router.delete("/trip", status_code=201)
def cancel_trip():
    return "create trip"


@router.get("/route", status_code=200)
def find_route():
    return "route info"

@router.delete("/route", status_code=200)
def cancel_route():
    return "route info"

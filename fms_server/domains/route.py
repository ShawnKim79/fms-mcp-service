from pydantic import BaseModel

class Route(BaseModel):
    uuid: str
    driver_name: str
    driver_phone: str
    departure: str
    start_at: str
    arrival: str
    max_passenger: int
    is_cancel: int
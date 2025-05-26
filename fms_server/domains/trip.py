from pydantic import BaseModel
from datetime import datetime

class trip(BaseModel):
    route_uuid: str
    passenger_uuid: str
    onboard:str
    onboard_at: datetime
    is_cancel: int
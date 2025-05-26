from pydantic import BaseModel

class Passenger(BaseModel):
    uuid: str
    name: str
    phone: str
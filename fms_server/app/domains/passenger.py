from pydantic import BaseModel, ConfigDict
from uuid import UUID

class Passenger(BaseModel):
    id: UUID | None = None
    password: str
    name: str
    nickname: str
    contact_info: str

    model_config = ConfigDict(from_attributes=True)

class ResponsePassenger(BaseModel):
    id: UUID | None = None
    name: str
    nickname: str
    contact_info: str

    model_config = ConfigDict(from_attributes=True)

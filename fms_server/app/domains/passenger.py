from pydantic import BaseModel
from uuid import UUID

class Passenger(BaseModel):
    id: UUID
    name: str
    contact_info: str

from pydantic import BaseModel, ConfigDict
from uuid import UUID

class Passenger(BaseModel):
    id: UUID | None = None
    name: str
    contact_info: str

    model_config = ConfigDict(from_attributes=True)

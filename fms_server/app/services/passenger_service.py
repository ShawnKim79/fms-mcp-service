from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from passlib.hash import pbkdf2_sha256

from domains.passenger import Passenger, ResponsePassenger
from domains.route import Route
from domains.trip import Trip
from controllers.dto.request_dto import RequestCreatePassenger
from models.model import PassengerDB, RouteDB, TripDB

class PassengerService:
    def __init__(self, session: Session):
        self.session: Session = session

    def create_passenger(self, passenger: Passenger) -> Passenger:
        try:
            hashed_password = pbkdf2_sha256.hash(passenger.password)
            passenger_db = PassengerDB(
                id = uuid4(),
                password = hashed_password,
                name = passenger.name,
                nickname = passenger.nickname,
                contact_info = passenger.contact_info
            )
            
            self.session.add(passenger_db)
            self.session.commit()
            self.session.refresh(passenger_db)
            return Passenger.model_validate(passenger_db)
        except Exception as e:
            print(f"Error creating passenger: {e}")
            self.session.rollback()
            return None

    def find_by_id(self, passenger_id: str):
        passenger_db:PassengerDB = self.session.query(PassengerDB).filter(PassengerDB.id == passenger_id).first()
        if passenger_db is None:
            return None
        return Passenger.model_validate(passenger_db)
        
    def find_by_nickname(self, nickname:str):
        passenger_db:PassengerDB = self.session.query(PassengerDB).filter(PassengerDB.nickname == nickname).first()
        if passenger_db is None:
            return None
        return Passenger.model_validate(passenger_db)

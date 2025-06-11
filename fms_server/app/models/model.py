from sqlalchemy import Column, UUID, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PassengerDB(Base):
    __tablename__ = "passenger"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
    contact_info = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class RouteDB(Base):
    __tablename__ = "route"

    id = Column(UUID, primary_key=True, index=True)
    driver_id = Column(UUID)
    car_plate_number = Column(String)
    departure_location_name = Column(String)
    departure_time = Column(DateTime)
    destination_location_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class TripDB(Base):
    __tablename__ = "trip"

    id = Column(UUID, primary_key=True, index=True)
    ride_route_id = Column(UUID)
    passenger_id = Column(UUID)
    pickup_request_location_name = Column(String)
    pickup_time = Column(DateTime)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
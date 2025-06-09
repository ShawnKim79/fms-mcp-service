import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Uuid, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from sqlalchemy.schema import MetaData

sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from app.domains.passenger import Passenger
from app.domains.route import Route
from app.domains.trip import trip as RideRequest

target_metadata = MetaData()
target_metadata.reflect = lambda bind, schema=None: None # Hack to prevent reflection

Passenger.__table__.to_metadata(target_metadata)
Route.__table__.to_metadata(target_metadata)
RideRequest.__table__.to_metadata(target_metadata)

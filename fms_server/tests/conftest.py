import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

from fms_server.app.main import app
from fms_server.app.models.model import Base
from fms_server.app.services.fms_service import FmsService
from fms_server.app.config.database import get_db_session

# 테스트용 데이터베이스 URL
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "fms_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "fms_password")
DB_NAME = os.environ.get("DB_NAME", "fms")

# 데이터베이스 URL 생성
TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# TEST_DATABASE_URL = "postgresql://user:password@localhost:5432/fms_test"

# 테스트용 엔진 생성
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def test_db():
    # 테스트 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=test_engine)
    yield
    # 테스트 데이터베이스 테이블 삭제
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    # 각 테스트마다 새로운 세션 생성
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def fms_service(db_session):
    # FmsService 인스턴스 생성
    return FmsService()

@pytest.fixture(scope="function")
def client(db_session):
    # 테스트 클라이언트 생성
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_passenger():
    return {
        "id": str(uuid4()),
        "name": "Test Passenger",
        "contact_info": "test@example.com"
    }

@pytest.fixture
def sample_route():
    return {
        "id": str(uuid4()),
        "driver_id": str(uuid4()),
        "car_plate_number": "TEST123",
        "departure_location_name": "Seoul",
        "departure_time": "2024-03-20T10:00:00",
        "destination_location_name": "Busan"
    }

@pytest.fixture
def sample_ride_request(sample_route, sample_passenger):
    return {
        "id": str(uuid4()),
        "ride_route_id": sample_route["id"],
        "passenger_id": sample_passenger["id"],
        "pickup_request_location_name": "Gangnam",
        "pickup_time": "2024-03-20T09:30:00",
        "is_approved": False
    } 
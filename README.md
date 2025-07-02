
## FMS 서버 기동
```
fms_server$ uvicorn app.main:app --reload
```
## DB 계정 생성
```
CREATE USER fms_user PASSWORD 'fms_password';
CREATE DATABASE fms OWNER fms_user;
```

## 테이블 생성 쿼리
```
CREATE TABLE passenger (
    id UUID PRIMARY KEY,
    name VARCHAR,
    contact_info VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE route (
    id UUID PRIMARY KEY,
    driver_id UUID,
    car_plate_number VARCHAR,
    departure_location_name VARCHAR,
    departure_time TIMESTAMP,
    destination_location_name VARCHAR,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE trip (
    id UUID PRIMARY KEY,
    ride_route_id UUID,
    passenger_id UUID,
    pickup_request_location_name VARCHAR,
    pickup_time TIMESTAMP,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```


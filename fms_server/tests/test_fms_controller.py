import pytest
from uuid import uuid4
from datetime import datetime, timedelta

def test_create_passenger(client, sample_passenger):
    response = client.post("/fms/passengers", json=sample_passenger)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_passenger["name"]
    assert data["contact_info"] == sample_passenger["contact_info"]

def test_create_ride_route(client, sample_route):
    response = client.post("/fms/ride_routes", json=sample_route)
    assert response.status_code == 201
    data = response.json()
    assert data["car_plate_number"] == sample_route["car_plate_number"]
    assert data["departure_location_name"] == sample_route["departure_location_name"]

def test_get_ride_route(client, sample_route):
    # 먼저 라우트 생성
    create_response = client.post("/fms/ride_routes", json=sample_route)
    route_id = create_response.json()["id"]
    
    # 생성된 라우트 조회
    response = client.get(f"/fms/ride_routes/{route_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == route_id
    assert data["car_plate_number"] == sample_route["car_plate_number"]

def test_get_nonexistent_ride_route(client):
    response = client.get(f"/fms/ride_routes/{uuid4()}")
    assert response.status_code == 404

def test_find_ride_routes(client, sample_route):
    # 먼저 라우트 생성
    client.post("/fms/ride_routes", json=sample_route)
    
    # 필터링 조건으로 라우트 검색
    response = client.get(
        "/fms/ride_routes",
        params={
            "departure_location_name": sample_route["departure_location_name"],
            "destination_location_name": sample_route["destination_location_name"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["departure_location_name"] == sample_route["departure_location_name"]

def test_update_ride_route(client, sample_route):
    # 먼저 라우트 생성
    create_response = client.post("/fms/ride_routes", json=sample_route)
    route_id = create_response.json()["id"]
    
    # 라우트 업데이트
    update_data = sample_route.copy()
    update_data["car_plate_number"] = "UPDATED123"
    
    response = client.put(f"/fms/ride_routes/{route_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["car_plate_number"] == "UPDATED123"

def test_delete_ride_route(client, sample_route):
    # 먼저 라우트 생성
    create_response = client.post("/fms/ride_routes", json=sample_route)
    route_id = create_response.json()["id"]
    
    # 라우트 삭제
    response = client.delete(f"/fms/ride_routes/{route_id}")
    assert response.status_code == 204
    
    # 삭제된 라우트 조회 시도
    get_response = client.get(f"/fms/ride_routes/{route_id}")
    assert get_response.status_code == 404

def test_create_ride_request(client, sample_ride_request):
    response = client.post("/fms/ride_requests", json=sample_ride_request)
    assert response.status_code == 201
    data = response.json()
    assert data["pickup_request_location_name"] == sample_ride_request["pickup_request_location_name"]
    assert data["is_approved"] == sample_ride_request["is_approved"]

def test_get_ride_request(client, sample_ride_request):
    # 먼저 요청 생성
    create_response = client.post("/fms/ride_requests", json=sample_ride_request)
    request_id = create_response.json()["id"]
    
    # 생성된 요청 조회
    response = client.get(f"/fms/ride_requests/{request_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert data["pickup_request_location_name"] == sample_ride_request["pickup_request_location_name"]

def test_find_ride_requests(client, sample_ride_request):
    # 먼저 요청 생성
    create_response = client.post("/fms/ride_requests", json=sample_ride_request)
    request_id = create_response.json()["id"]
    
    # 필터링 조건으로 요청 검색
    response = client.get(
        "/fms/ride_requests",
        params={
            "ride_route_id": sample_ride_request["ride_route_id"],
            "is_approved": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["id"] == request_id

def test_approve_ride_request(client, sample_ride_request):
    # 먼저 요청 생성
    create_response = client.post("/fms/ride_requests", json=sample_ride_request)
    request_id = create_response.json()["id"]
    
    # 요청 승인
    response = client.put(f"/fms/ride_requests/{request_id}/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == request_id
    assert data["is_approved"] == True 

def test_involve_driver_to_route(client, sample_route):
    # 먼저 라우트 생성
    create_response = client.post("/fms/ride_routes", json=sample_route)
    route_id = create_response.json()["id"]
    
    # 드라이버 포함시키기
    involve_driver_data = {
        "driver_id": "test_driver"
    }
    
    response = client.put(f"/fms/ride_routes/{route_id}/involve_driver", json=involve_driver_data)
    assert response.status_code == 200
    data = response.json()
    assert data["driver_id"] == "test_driver"

def test_involve_driver_to_nonexistent_route(client):
    # 존재하지 않는 라우트에 드라이버 포함시키기
    involve_driver_data = {
        "driver_id": "test_driver"
    }
    
    response = client.put(f"/fms/ride_routes/{uuid4()}/involve_driver", json=involve_driver_data)
    assert response.status_code == 404 
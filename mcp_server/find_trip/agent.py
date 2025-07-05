import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    if city.lower() == "seoul":
        return {
            "status": "success",
            "report": (
                "좀 거시기 합니다."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

def create_passenger(name: str, contact_info: str) -> Dict[str, Any]:
    """
    시스템에 새로운 승객을 등록합니다.

    Args:
        name (str): 승객의 이름.
        contact_info (str): 승객의 연락처 정보 (예: 전화번호, 이메일).

    Returns:
        Dict[str, Any]: 생성된 승객 정보 (id, name, contact_info).
    """
    endpoint = f"{BASE_URL}/fms/passengers"
    payload = {"name": name, "contact_info": contact_info}
    print(f"API 호출: POST {endpoint} | 데이터: {payload}")
    # response = requests.post(endpoint, json=payload)
    # response.raise_for_status()
    # return response.json()
    # 아래는 모의(mock) 반환 데이터입니다.
    return {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "name": name, "contact_info": contact_info}

def create_ride_route(driver_id: str, car_plate_number: str, departure_location_name: str, departure_time: str, destination_location_name: str) -> Dict[str, Any]:
    """
    운전자를 위한 새로운 운행 경로를 생성합니다.

    Args:
        driver_id (str): 운전자의 고유 ID (UUID).
        car_plate_number (str): 차량 번호판.
        departure_location_name (str): 출발지 이름.
        departure_time (str): 출발 시간 (ISO 8601 형식, 예: '2025-07-05T10:00:00Z').
        destination_location_name (str): 목적지 이름.

    Returns:
        Dict[str, Any]: 생성된 경로 정보.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes"
    payload = {
        "driver_id": driver_id,
        "car_plate_number": car_plate_number,
        "departure_location_name": departure_location_name,
        "departure_time": departure_time,
        "destination_location_name": destination_location_name
    }
    print(f"API 호출: POST {endpoint} | 데이터: {payload}")
    # response = requests.post(endpoint, json=payload)
    # response.raise_for_status()
    # return response.json()
    payload['id'] = "r1b2c3d4-e5f6-7890-1234-567890abcdef"
    return payload

def find_ride_routes(driver_id: Optional[str] = None, start_time: Optional[str] = None, end_time: Optional[str] = None, departure_location_name: Optional[str] = None, destination_location_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    지정된 조건에 맞는 운행 경로를 검색합니다.

    Args:
        driver_id (Optional[str]): 검색할 운전자의 ID.
        start_time (Optional[str]): 검색할 출발 시간 범위의 시작 (ISO 8601).
        end_time (Optional[str]): 검색할 출발 시간 범위의 끝 (ISO 8601).
        departure_location_name (Optional[str]): 검색할 출발지 이름.
        destination_location_name (Optional[str]): 검색할 목적지 이름.

    Returns:
        List[Dict[str, Any]]: 검색된 경로 목록.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes"
    params = {
        "driver_id": driver_id,
        "start_time": start_time,
        "end_time": end_time,
        "departure_location_name": departure_location_name,
        "destination_location_name": destination_location_name
    }
    # None 값을 가진 파라미터는 제거
    params = {k: v for k, v in params.items() if v is not None}
    print(f"API 호출: GET {endpoint} | 파라미터: {params}")
    # response = requests.get(endpoint, params=params)
    # response.raise_for_status()
    # return response.json()
    return [{
        "id": "r1b2c3d4-e5f6-7890-1234-567890abcdef",
        "driver_id": driver_id or "d_-e5f6-7890-1234-567890abcdef",
        "car_plate_number": "12가 3456",
        "departure_location_name": departure_location_name or "강남역",
        "departure_time": "2025-07-05T11:00:00Z",
        "destination_location_name": destination_location_name or "판교역"
    }]

def get_ride_route(route_id: str) -> Dict[str, Any]:
    """
    특정 경로의 상세 정보를 조회합니다.

    Args:
        route_id (str): 조회할 경로의 고유 ID (UUID).

    Returns:
        Dict[str, Any]: 경로 상세 정보.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes/{route_id}"
    print(f"API 호출: GET {endpoint}")
    # response = requests.get(endpoint)
    # response.raise_for_status()
    # return response.json()
    return {
        "id": route_id,
        "driver_id": "d_a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "car_plate_number": "12가 3456",
        "departure_location_name": "강남역",
        "departure_time": "2025-07-05T11:00:00Z",
        "destination_location_name": "판교역"
    }

def create_trip(ride_route_id: str, passenger_id: str, pickup_request_location_name: str, pickup_time: str) -> Dict[str, Any]:
    """
    승객이 특정 경로에 대한 탑승(여정)을 요청합니다.

    Args:
        ride_route_id (str): 탑승할 경로의 ID.
        passenger_id (str): 탑승할 승객의 ID.
        pickup_request_location_name (str): 승객이 탑승을 원하는 위치.
        pickup_time (str): 승객이 탑승을 원하는 시간 (ISO 8601).

    Returns:
        Dict[str, Any]: 생성된 여정 요청 정보 (승인 상태는 'false'로 시작).
    """
    endpoint = f"{BASE_URL}/fms/trips"
    payload = {
        "ride_route_id": ride_route_id,
        "passenger_id": passenger_id,
        "pickup_request_location_name": pickup_request_location_name,
        "pickup_time": pickup_time
    }
    print(f"API 호출: POST {endpoint} | 데이터: {payload}")
    # response = requests.post(endpoint, json=payload)
    # response.raise_for_status()
    # return response.json()
    payload['id'] = "t1b2c3d4-e5f6-7890-1234-567890abcdef"
    payload['is_approved'] = False
    return payload

def get_trip(request_id: str) -> Dict[str, Any]:
    """
    특정 여정 요청의 상세 정보를 조회합니다.

    Args:
        request_id (str): 조회할 여정의 고유 ID (UUID).

    Returns:
        Dict[str, Any]: 여정 상세 정보.
    """
    endpoint = f"{BASE_URL}/fms/trips/{request_id}"
    print(f"API 호출: GET {endpoint}")
    # response = requests.get(endpoint)
    # response.raise_for_status()
    # return response.json()
    return {
        "id": request_id,
        "ride_route_id": "r1b2c3d4-e5f6-7890-1234-567890abcdef",
        "passenger_id": "p_a1b2c3d4-e5f6-7890-1234-567890abcdef",
        "pickup_request_location_name": "강남역 5번 출구",
        "pickup_time": "2025-07-05T10:55:00Z",
        "is_approved": False
    }

def approve_trip(request_id: str) -> Dict[str, Any]:
    """
    특정 여정 요청을 승인합니다.

    Args:
        request_id (str): 승인할 여정의 고유 ID (UUID).

    Returns:
        Dict[str, Any]: 승인 상태가 업데이트된 여정 정보.
    """
    endpoint = f"{BASE_URL}/fms/trips/{request_id}/approve"
    print(f"API 호출: PUT {endpoint}")
    # response = requests.put(endpoint)
    # response.raise_for_status()
    # return response.json()
    trip_data = get_trip(request_id)
    trip_data['is_approved'] = True
    return trip_data

root_agent = Agent(
    name="ride_sharing_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 라이드 쉐어링 시스템을 관리하는 에이전트입니다."
    ),
    instruction=(
        """
        에이전트는 라이드 쉐어링 시스템을 관리하는 에이전트입니다.
        라이드 쉐어링 시스템은 운전자와 승객이 탑승 요청을 할 수 있는 시스템입니다.
        운전자는 운행 경로를 생성하고, 승객은 운행 경로를 조회하고, 탑승 요청을 할 수 있습니다.
        운전자는 승객의 탑승 요청을 승인하거나 거절할 수 있습니다.
        
        """
    ),
    tools=[get_weather, get_current_time, create_passenger, create_ride_route, find_ride_routes, get_ride_route, create_trip, get_trip, approve_trip],
)

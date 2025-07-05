import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"


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

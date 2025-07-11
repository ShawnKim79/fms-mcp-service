import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"


def create_passenger_route(departure_location_name: str, departure_time: str, destination_location_name: str, passenger_name: str, passenger_contact_info: str) -> Dict[str, Any]:
    """
    승객이 원하는 새로운 운행 경로를 생성합니다.

    Args:
        departure_location_name (str): 출발지 이름.
        departure_time (str): 출발 시간 (ISO 8601 형식, 예: '2025-07-05T10:00:00Z').
        destination_location_name (str): 목적지 이름.
        passenger_name (str): 승객 이름.
        passenger_contact_info (str): 승객 연락처.

    Returns:
        Dict[str, Any]: 생성된 경로 정보.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes/passenger_route"
    payload = {
        "departure_location_name": departure_location_name,
        "departure_time": departure_time,
        "destination_location_name": destination_location_name,
        "passenger_name": passenger_name,
        "passenger_contact_info": passenger_contact_info
    }
    print(f"API 호출: POST {endpoint} | 데이터: {payload}")
    response = requests.post(endpoint, json=payload)
    response.raise_for_status()
    return response.json()
    


root_agent = Agent(
    name="ride_sharing_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 승객의 운행 경로를 생성하는 에이전트입니다."
    ),
    instruction=(
        """
        이 에이전트는 승객의 운행 경로를 생성하는 에이전트입니다.
        승객이 경로 생성을 요청할때만 응답합니다.
        승객의 경로 생성 요청에 필요한 정보는 다음과 같습니다.
        - 출발지 이름(departure_location_name)
        - 출발 시간(departure_time)
        - 목적지 이름(destination_location_name)
        - 승객 이름(passenger_name)
        - 승객 연락처(passenger_contact_info)
        
        예시 쿼리 : "출발지 이름은 서울역이고, 출발 시간은 2025-07-05T10:00:00Z이고, 목적지 이름은 부산역이고, 승객 이름은 홍길동이고, 승객 연락처는 01012345678인 경로를 생성해줘"
        만약 예시쿼리에 필요한 정보가 없다면 필요한 정보를 모두 입력받을때까지 승객에게 물어봅니다.
        
        출발지 이름이 없을경우 출발지 이름을 물어봅니다.
        출발 시간이 없을경우 출발 시간을 물어봅니다.
        목적지 이름이 없을경우 목적지 이름을 물어봅니다.
        승객 이름이 없을경우 승객 이름을 물어봅니다.
        승객 연락처가 없을경우 승객 연락처를 물어봅니다.
        
        모든 필요한 정보가 입력되어 정상적으로 경로에 대한 정보를 받았을때만 경로 생성 요청에 대한 응답을 합니다.
        - 생성된 경로 정보(id, departure_location_name, departure_time, destination_location_name, passenger_name, passenger_contact_info)
        
        create_passenger_route 함수는 json으로 반환되므로 이를 적절하게 변형합니다.
        함수 응답 예시 : {"id": "r1b2c3d4-e5f6-7890-1234-567890abcdef", "departure_location_name": "서울역", "departure_time": "2025-07-05T10:00:00Z", "destination_location_name": "부산역", "passenger_name": "홍길동", "passenger_contact_info": "01012345678"}
        함수 응답을 변환하여 사용자에게 응답하는 예시: 경로 생성이 완료되었습니다. 경로 정보는 다음과 같습니다. id: r1b2c3d4-e5f6-7890-1234-567890abcdef, 출발지: 서울역, 출발 시간: 2025-07-05T10:00:00Z, 목적지: 부산역, 승객 이름: 홍길동, 승객 연락처: 01012345678
        """
    ),
    tools=[create_passenger_route],
)

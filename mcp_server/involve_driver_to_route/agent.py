import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"


def involve_driver_to_route(route_id: str, driver_id: str, car_plate_number: str, driver_name: str, driver_contact_info: str) -> Dict[str, Any]:
    """
    생성되어 있는 운행 경로에 운전자를 추가합니다.

    Args:
        route_id (str): 운행 경로의 고유 ID (UUID).
        driver_id (str): 운전자의 고유 ID (UUID).
        car_plate_number (str): 차량 번호판.
        driver_name (str): 운전자 이름.
        driver_contact_info (str): 운전자 연락처.

    Returns:
        Dict[str, Any]: 생성된 경로 정보.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes/{route_id}/involve_driver"
    payload = {
        "driver_id": driver_id,
        "car_plate_number": car_plate_number,
        "driver_name": driver_name,
        "driver_contact_info": driver_contact_info
    }
    print(f"API 호출: POST {endpoint} | 데이터: {payload}")
    response = requests.put(endpoint, json=payload)
    response.raise_for_status()
    return response.json()
    # payload['id'] = "r1b2c3d4-e5f6-7890-1234-567890abcdef"
    # return payload



root_agent = Agent(
    name="ride_sharing_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 승객이 생성한 운행경로에 운전자를 추가하는 에이전트입니다."
    ),
    instruction=(
        """
        이 에이전트는 승객이 생성한 운행경로에 운전자를 추가하는 에이전트입니다.
        승객이 운행경로 생성을 요청할때만 응답합니다.
        승객의 운행경로 생성 요청에 필요한 정보는 다음과 같습니다.
        - 운행 경로 ID(route_id)
        - 운전자 ID(driver_id)
        - 차량 번호판(car_plate_number)
        - 운전자 이름(driver_name)
        - 운전자 연락처(driver_contact_info)
        
        예시 쿼리 : "운행 경로 ID는 123e4567-e89b-12d3-a456-426614174000이고, 운전자 ID는 123e4567-e89b-12d3-a456-426614174000이고, 차량 번호판은 1234가나다이고, 운전자 이름은 홍길동이고, 운전자 연락처는 01012345678인 운행경로에 운전자를 추가해줘"
        만약 예시쿼리에 필요한 정보가 없다면 필요한 정보를 모두 입력받을때까지 승객에게 물어봅니다.
        
        운행 경로 ID가 없을경우 운행 경로 ID를 물어봅니다.
        운전자 ID가 없을경우 운전자 ID를 물어봅니다.
        차량 번호판이 없을경우 차량 번호판을 물어봅니다.
        운전자 이름이 없을경우 운전자 이름을 물어봅니다.
        운전자 연락처가 없을경우 운전자 연락처를 물어봅니다.
        """
    ),
    tools=[involve_driver_to_route],
)


import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent

from mcp_server.find_route.agent import find_ride_routes
from mcp_server.involve_driver_to_route.agent import involve_driver_to_route

BASE_URL = "http://localhost:8001"


def find_and_involve_driver(
    driver_id: str,
    car_plate_number: str,
    driver_name: str,
    driver_contact_info: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    departure_location_name: Optional[str] = None,
    destination_location_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    경로를 검색하고, 경로가 존재하면 운전자를 등록합니다.

    Args:
        driver_id (str): 운전자의 고유 ID (UUID).
        car_plate_number (str): 차량 번호판.
        driver_name (str): 운전자 이름.
        driver_contact_info (str): 운전자 연락처.
        start_time (Optional[str]): 검색할 출발 시간 범위의 시작 (ISO 8601).
        end_time (Optional[str]): 검색할 출발 시간 범위의 끝 (ISO 8601).
        departure_location_name (Optional[str]): 검색할 출발지 이름.
        destination_location_name (Optional[str]): 검색할 목적지 이름.

    Returns:
        Dict[str, Any]: 처리 결과 메시지.
    """
    routes = find_ride_routes(
        start_time=start_time,
        end_time=end_time,
        departure_location_name=departure_location_name,
        destination_location_name=destination_location_name,
    )

    if not routes:
        return {"message": "해당 조건에 맞는 경로를 찾을 수 없습니다."}

    # 첫 번째 경로에 운전자를 등록합니다.
    route_id = routes[0]["id"]
    
    try:
        result = involve_driver_to_route(
            route_id=route_id,
            driver_id=driver_id,
            car_plate_number=car_plate_number,
            driver_name=driver_name,
            driver_contact_info=driver_contact_info,
        )
        return {"message": "운전자 등록에 성공했습니다.", "data": result}
    except Exception as e:
        return {"message": f"운전자 등록에 실패했습니다: {e}"}


root_agent = Agent(
    name="ride_sharing_orchestrator_agent",
    model="gemini-2.0-flash",
    description="운행 경로를 검색하고 운전자를 등록하는 작업을 조율하는 에이전트입니다.",
    instruction=(
        """
        이 에이전트는 사용자의 요청에 따라 운행 경로를 찾고, 해당 경로에 운전자를 등록하는 역할을 합니다.
        그 외의 요청에 대해서는 무시합니다.
        
        사용자 요청 예시:
        "출발지 서울역, 목적지 부산역인 경로를 찾아서, 운전자 ID 123, 차량번호 12가3456, 이름 김기사, 연락처 010-1111-2222 정보를 등록해줘."

        에이전트는 다음 두 단계를 순서대로 실행합니다.
        1. `find_ride_routes`를 호출하여 조건에 맞는 경로를 검색합니다.
        2. 경로가 존재하면, 첫 번째 검색된 경로의 ID를 사용하여 `involve_driver_to_route`를 호출하고 운전자를 등록합니다.

        경로가 없거나 운전자 등록에 실패하면, 사용자에게 해당 상황을 명확하게 알려줍니다.
        """
    ),
    tools=[find_and_involve_driver],
)

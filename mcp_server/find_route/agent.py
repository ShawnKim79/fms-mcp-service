import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
import requests
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"



def find_ride_routes(start_time: Optional[str] = None, end_time: Optional[str] = None, departure_location_name: Optional[str] = None, destination_location_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    지정된 조건에 맞는 운행 경로를 검색합니다.

    Args:
        start_time (Optional[str]): 검색할 출발 시간 범위의 시작 (ISO 8601).
        end_time (Optional[str]): 검색할 출발 시간 범위의 끝 (ISO 8601).
        departure_location_name (Optional[str]): 검색할 출발지 이름.
        destination_location_name (Optional[str]): 검색할 목적지 이름.

    Returns:
        List[Dict[str, Any]]: 검색된 경로 목록.
    """
    endpoint = f"{BASE_URL}/fms/ride_routes"
    params = {
        "start_time": start_time,
        "end_time": end_time,
        "departure_location_name": departure_location_name,
        "destination_location_name": destination_location_name
    }
    # None 값을 가진 파라미터는 제거
    params = {k: v for k, v in params.items() if v is not None}
    print(f"API 호출: GET {endpoint} | 파라미터: {params}")
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    return response.json()
    

root_agent = Agent(
    name="ride_sharing_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 생성된 운행 경로를 조회하는 에이전트입니다."
    ),
    instruction=(
        """
        에이전트는 생성된 운행 경로를 조회하는 에이전트입니다.
        운행경로에 대한 조회가 아닌 요청은 응답하지 않습니다.

        조회할 운행 경로의 조건은 다음과 같습니다.
        - 출발 시간(start_time)
        - 출발 시간(end_time)
        - 출발지 이름(departure_location_name)
        - 목적지 이름(destination_location_name)
        
        만약 예시쿼리에 필요한 정보가 없다면 전체 운행경로를 조회합니다.
        전체 운행경로 조회 예시 : "전체 운행경로를 조회해줘"

        운행 경로가 주어지는 쿼리의 모습은 다음과 같습니다.
        예시 쿼리 : "출발지 이름은 서울역이고, 출발 시간은 2025-07-05T10:00:00Z이고, 목적지 이름은 부산역인 경로를 조회해줘"
        
        조회된 운행 경로는 json 형태로 반환되므로 이를 적절하게 변형합니다.
        함수 응답 예시 : [{"id": "r1b2c3d4-e5f6-7890-1234-567890abcdef", "departure_location_name": "서울역", "departure_time": "2025-07-05T10:00:00Z", "destination_location_name": "부산역", "passenger_name": "홍길동", "passenger_contact_info": "01012345678"}]
        함수 응답을 변환하여 사용자에게 응답하는 예시: 조회된 운행 경로는 다음과 같습니다. id: r1b2c3d4-e5f6-7890-1234-567890abcdef, 출발지: 서울역, 출발 시간: 2025-07-05T10:00:00Z, 목적지: 부산역, 승객 이름: 홍길동, 승객 연락처: 01012345678
        """
    ),
    tools=[find_ride_routes],
)

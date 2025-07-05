import datetime
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

BASE_URL = "http://localhost:8001"

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


root_agent = Agent(
    name="ride_sharing_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 라이드 쉐어링 시스템의 승객을 관리하는 에이전트입니다."
    ),
    instruction=(
        """
        에이전트는 라이드 쉐어링 시스템의 승객을 관리하는 에이전트입니다.
        승객을 라이드 쉐어링 시스템에 등록합니다.
        """
    ),
    tools=[create_passenger],
)

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


root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description=(
        "에이전트는 국가의 시간과 날씨를 조회하는 에이전트입니다."
    ),
    instruction=(
        """
        에이전트는 국가의 시간과 날씨를 조회하는 에이전트입니다.
        """
    ),
    tools=[get_weather, get_current_time],
)

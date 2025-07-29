"""
슬랙 이벤트 API로부터 이벤트를 수신하고 처리하는 컨트롤러
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Dict, Any
import logging

from services.slack_service import SlackService
from services.mcp_service import MCPService
from services.command_service import CommandService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/slack/events")
async def slack_events(request: Request, 
                       slack_service: SlackService = Depends(),
                       mcp_service: MCPService = Depends()) -> Dict[str, Any]:
    """
    슬랙 이벤트 API로부터 이벤트를 수신하고 처리하는 엔드포인트
    
    Args:
        request: FastAPI Request 객체
        slack_service: 슬랙 서비스 인스턴스
        mcp_service: MCP 서비스 인스턴스
        
    Returns:
        Dict[str, Any]: 응답 메시지
    """
    # 요청 본문 파싱
    payload = await request.json()
    
    # 슬랙 이벤트 타입 확인
    if "type" not in payload:
        raise HTTPException(status_code=400, detail="Invalid request")
    
    # URL 검증 요청 처리
    if payload["type"] == "url_verification":
        return {"challenge": payload["challenge"]}
    
    # 이벤트 콜백 처리
    if payload["type"] == "event_callback":
        event = payload.get("event", {})
        event_type = event.get("type")
        
        # 메시지 이벤트 처리
        if event_type == "message":
            # 봇 메시지 무시
            if event.get("bot_id"):
                return {"status": "ok"}
            
            user_id = event.get("user")
            text = event.get("text")
            channel = event.get("channel")
            
            if not user_id or not text:
                return {"status": "ok"}
            
            # 사용자 정보 조회
            user_info = await slack_service.get_user_info(user_id)
            
            # 명령어 처리 - 슬랙봇 자체에서 처리할 기본 명령어만 처리
            command_service = CommandService(slack_service, mcp_service)
            command_response = await command_service.process_message(user_id, text, channel)
            
            if command_response:
                # 명령어가 처리된 경우 응답 메시지 전송
                await slack_service.send_message(channel, command_response)
            else:
                # 명령어가 아닌 경우 MCP 서버로 메시지 중계
                # 모든 라이드 셰어링 관련 비즈니스 로직은 MCP 서버의 에이전트가 처리
                await mcp_service.relay_message(
                    user_id=user_id,
                    user_name=user_info.get("name", "Unknown User"),
                    message=text,
                    channel_id=channel
                )
            
            return {"status": "ok"}
        
        # 사용자 참여 이벤트 처리
        elif event_type == "member_joined_channel":
            user_id = event.get("user")
            channel = event.get("channel")
            
            # 환영 메시지 전송
            welcome_message = f"안녕하세요! 라이드 셰어링 봇입니다. '도움말' 명령어를 입력하시면 사용 가능한 명령어 목록을 확인하실 수 있습니다."
            await slack_service.send_message(channel, welcome_message)
            
            return {"status": "ok"}
    
    return {"status": "ok"}
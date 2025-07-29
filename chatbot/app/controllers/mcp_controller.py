"""
MCP 서버로부터의 웹훅을 처리하는 컨트롤러
"""
from fastapi import APIRouter, Request, Depends, HTTPException
from typing import Dict, Any

from services.slack_service import SlackService

router = APIRouter()

@router.post("/mcp/webhook")
async def mcp_webhook(request: Request, 
                      slack_service: SlackService = Depends()) -> Dict[str, Any]:
    """
    MCP 서버로부터의 웹훅을 처리하는 엔드포인트
    
    Args:
        request: FastAPI Request 객체
        slack_service: 슬랙 서비스 인스턴스
        
    Returns:
        Dict[str, Any]: 응답 메시지
    """
    # 요청 본문 파싱
    payload = await request.json()
    
    # 필수 필드 검증
    if "user_id" not in payload or "message" not in payload:
        raise HTTPException(status_code=400, detail="Invalid webhook data")
    
    # 사용자에게 메시지 전송
    user_id = payload["user_id"]
    message = payload["message"]
    
    # 채널 ID가 제공된 경우 해당 채널로 메시지 전송, 그렇지 않으면 사용자에게 DM 전송
    channel_id = payload.get("channel_id")
    
    if channel_id:
        await slack_service.send_message(channel_id, message)
    else:
        # 사용자에게 DM 전송
        await slack_service.send_direct_message(user_id, message)
    
    return {"status": "ok"}
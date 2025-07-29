"""
사용자 세션 정보를 저장하는 모델
"""
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class SessionModel(BaseModel):
    """사용자 세션 정보를 저장하는 모델 클래스"""
    
    user_id: str = Field(..., description="사용자 ID")
    conversation_state: str = Field(default="initial", description="대화 상태")
    last_interaction: datetime = Field(default_factory=datetime.now, description="마지막 상호작용 시간")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="기타 메타데이터")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "U01234567",
                "conversation_state": "awaiting_destination",
                "last_interaction": "2025-07-19T12:00:00",
                "metadata": {
                    "ride_request_id": "R01234567"
                }
            }
        }
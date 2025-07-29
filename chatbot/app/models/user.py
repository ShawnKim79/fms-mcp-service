"""
사용자 정보를 저장하는 모델
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    """사용자 정보를 저장하는 모델 클래스"""
    
    id: str = Field(..., description="슬랙 사용자 ID")
    name: str = Field(..., description="사용자 이름")
    email: Optional[str] = Field(None, description="사용자 이메일")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    
    class Config:
        schema_extra = {
            "example": {
                "id": "U01234567",
                "name": "John Doe",
                "email": "john.doe@example.com",
                "created_at": "2025-07-19T12:00:00"
            }
        }
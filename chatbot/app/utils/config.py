"""
설정 관리 유틸리티
"""
import os
from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings

absolute_path = os.path.abspath('.')
print(absolute_path)

class Settings(BaseSettings):
    """애플리케이션 설정 클래스"""
    
    # 슬랙 API 설정
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str
    
    # MCP 서버 설정
    MCP_API_URL: str
    MCP_API_KEY: str
    
    # 애플리케이션 설정
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: Optional[str] = None
    
    class Config:
        env_file = f"{absolute_path}/chatbot/.env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    애플리케이션 설정을 반환합니다.
    
    Returns:
        Settings: 애플리케이션 설정 인스턴스
    """
    return Settings()
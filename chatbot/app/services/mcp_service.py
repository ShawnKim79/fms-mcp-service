"""
MCP 서버와의 통신을 담당하는 서비스
"""
from typing import Dict, Any, Optional
import logging
import httpx
from datetime import datetime

from utils.config import get_settings

logger = logging.getLogger(__name__)

class MCPService:
    """MCP 서버와의 통신을 담당하는 서비스 클래스"""
    
    def __init__(self):
        """MCPService 초기화"""
        settings = get_settings()
        self.api_url = settings.MCP_API_URL
        self.api_key = settings.MCP_API_KEY
    
    async def check_connection(self) -> bool:
        """
        MCP 서버와의 연결 상태를 확인합니다.
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            # MCP 서버의 헬스 체크 엔드포인트 호출
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.api_url}/health",
                    headers=headers,
                    timeout=5.0
                )
                response.raise_for_status()
                return True
        except Exception as e:
            logger.error(f"MCP server connection check failed: {e}")
            return False
    
    async def relay_message(self, user_id: str, user_name: str, message: str, 
                           channel_id: Optional[str] = None) -> Dict[str, Any]:
        """
        사용자 메시지를 MCP 서버로 중계합니다.
        
        Args:
            user_id: 사용자 ID
            user_name: 사용자 이름
            message: 원본 메시지 내용
            channel_id: 메시지가 수신된 채널 ID (선택 사항)
            
        Returns:
            Dict[str, Any]: MCP 서버 응답
        """
        try:
            # MCP 서버로 전송할 데이터 구성
            payload = {
                "user_id": user_id,
                "user_name": user_name,
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }
            
            if channel_id:
                payload["channel_id"] = channel_id
            
            # MCP 서버로 데이터 전송
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/api/messages",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"Error relaying message to MCP server: {e}")
            raise
    
    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        MCP 서버로부터의 웹훅 데이터를 처리합니다.
        
        Args:
            webhook_data: 웹훅 데이터
            
        Returns:
            Dict[str, Any]: 처리 결과
        """
        # 웹훅 데이터 검증 및 처리 로직
        # 현재는 단순히 데이터를 반환
        return webhook_data
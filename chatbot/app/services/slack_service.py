"""
슬랙 API와의 통신을 담당하는 서비스
"""
from typing import Dict, Any, Optional
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from utils.config import get_settings

logger = logging.getLogger(__name__)

class SlackService:
    """슬랙 API와의 통신을 담당하는 서비스 클래스"""
    
    def __init__(self):
        """SlackService 초기화"""
        settings = get_settings()
        self.client = WebClient(token=settings.SLACK_BOT_TOKEN)
    
    async def send_message(self, channel_id: str, text: str) -> Dict[str, Any]:
        """
        지정된 채널에 메시지를 전송합니다.
        
        Args:
            channel_id: 메시지를 전송할 채널 ID
            text: 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 슬랙 API 응답
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel_id,
                text=text
            )
            return response
        except SlackApiError as e:
            logger.error(f"Error sending message: {e}")
            raise
    
    async def send_direct_message(self, user_id: str, text: str) -> Dict[str, Any]:
        """
        사용자에게 다이렉트 메시지를 전송합니다.
        
        Args:
            user_id: 메시지를 전송할 사용자 ID
            text: 전송할 메시지 내용
            
        Returns:
            Dict[str, Any]: 슬랙 API 응답
        """
        try:
            # 사용자와의 DM 채널 열기
            response = self.client.conversations_open(users=user_id)
            channel_id = response["channel"]["id"]
            
            # 메시지 전송
            return await self.send_message(channel_id, text)
        except SlackApiError as e:
            logger.error(f"Error sending direct message: {e}")
            raise
    
    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """
        사용자 정보를 조회합니다.
        
        Args:
            user_id: 조회할 사용자 ID
            
        Returns:
            Dict[str, Any]: 사용자 정보
        """
        try:
            response = self.client.users_info(user=user_id)
            return response["user"]
        except SlackApiError as e:
            logger.error(f"Error getting user info: {e}")
            raise
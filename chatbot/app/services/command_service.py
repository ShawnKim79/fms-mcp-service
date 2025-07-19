"""
슬랙 명령어 처리를 담당하는 서비스
"""
from typing import Dict, Any, Optional
import logging
import re

from services.slack_service import SlackService
from services.mcp_service import MCPService

logger = logging.getLogger(__name__)

class CommandService:
    """슬랙 명령어 처리를 담당하는 서비스 클래스"""
    
    def __init__(self, 
                 slack_service: SlackService,
                 mcp_service: MCPService):
        """
        CommandService 초기화
        
        Args:
            slack_service: 슬랙 서비스 인스턴스
            mcp_service: MCP 서비스 인스턴스
        """
        self.slack_service = slack_service
        self.mcp_service = mcp_service
        
        # 명령어 패턴 정의 - 슬랙봇 자체에서 처리할 기본 명령어만 정의
        self.command_patterns = {
            r"^도움말$|^help$|^명령어$": self.help_command,
            r"^봇 상태$|^bot status$": self.bot_status_command,
        }
    
    async def process_message(self, user_id: str, text: str, channel_id: str) -> Optional[str]:
        """
        사용자 메시지를 처리하고 명령어인 경우 해당 명령어를 실행합니다.
        슬랙봇 자체에서 처리할 기본 명령어만 처리하고, 나머지는 MCP 서버로 중계합니다.
        
        Args:
            user_id: 사용자 ID
            text: 메시지 내용
            channel_id: 채널 ID
            
        Returns:
            Optional[str]: 명령어 처리 결과 메시지 (명령어가 아닌 경우 None)
        """
        # 명령어 패턴 매칭
        for pattern, handler in self.command_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                logger.info(f"Command detected: {text}")
                return await handler(user_id, text, channel_id)
        
        # 명령어가 아닌 경우 None 반환
        return None
    
    async def help_command(self, user_id: str, text: str, channel_id: str) -> str:
        """
        도움말 명령어 처리
        
        Args:
            user_id: 사용자 ID
            text: 메시지 내용
            channel_id: 채널 ID
            
        Returns:
            str: 도움말 메시지
        """
        help_message = """
*슬랙봇 명령어*

• *도움말* 또는 *help*: 사용 가능한 명령어 목록을 보여줍니다.
• *봇 상태* 또는 *bot status*: 슬랙봇의 현재 연결 상태를 확인합니다.

라이드 셰어링과 관련된 모든 질문이나 요청은 자연스럽게 대화하듯이 입력해주세요.
MCP 서버의 AI 에이전트가 처리하여 응답해 드립니다.
"""
        return help_message
    
    async def bot_status_command(self, user_id: str, text: str, channel_id: str) -> str:
        """
        봇 상태 명령어 처리
        
        Args:
            user_id: 사용자 ID
            text: 메시지 내용
            channel_id: 채널 ID
            
        Returns:
            str: 봇 상태 메시지
        """
        # MCP 서버 연결 상태 확인
        try:
            # 간단한 핑 요청으로 MCP 서버 연결 상태 확인
            await self.mcp_service.check_connection()
            mcp_status = "연결됨 ✅"
        except Exception as e:
            logger.error(f"MCP server connection error: {e}")
            mcp_status = "연결 오류 ❌"
        
        status_message = f"""
*슬랙봇 상태*

• 슬랙 API: 연결됨 ✅
• MCP 서버: {mcp_status}
• 봇 버전: 1.0.0
"""
        return status_message
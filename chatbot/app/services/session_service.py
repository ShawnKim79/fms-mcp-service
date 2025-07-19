"""
사용자 세션을 관리하는 서비스
"""
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SessionService:
    """사용자 세션을 관리하는 서비스 클래스"""
    
    def __init__(self):
        """SessionService 초기화"""
        # 메모리 기반 세션 저장소 (실제 구현에서는 Redis 등 외부 저장소 사용 권장)
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = timedelta(hours=1)  # 세션 타임아웃: 1시간
    
    async def get_or_create_session(self, user_id: str) -> Dict[str, Any]:
        """
        사용자 세션을 조회하거나 생성합니다.
        
        Args:
            user_id: 사용자 ID
            
        Returns:
            Dict[str, Any]: 사용자 세션 데이터
        """
        # 세션이 존재하는 경우 반환
        if user_id in self.sessions:
            session = self.sessions[user_id]
            # 세션 만료 확인
            if datetime.now() - session["last_interaction"] <= self.session_timeout:
                # 세션 갱신
                session["last_interaction"] = datetime.now()
                return session
        
        # 세션이 없거나 만료된 경우 새로 생성
        session = {
            "user_id": user_id,
            "conversation_state": "initial",
            "last_interaction": datetime.now(),
            "metadata": {}
        }
        self.sessions[user_id] = session
        return session
    
    async def update_session(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        사용자 세션을 업데이트합니다.
        
        Args:
            user_id: 사용자 ID
            data: 업데이트할 데이터
            
        Returns:
            Dict[str, Any]: 업데이트된 세션 데이터
        """
        # 세션이 없는 경우 생성
        if user_id not in self.sessions:
            await self.get_or_create_session(user_id)
        
        # 세션 업데이트
        session = self.sessions[user_id]
        session.update(data)
        session["last_interaction"] = datetime.now()
        
        return session
    
    async def clear_session(self, user_id: str) -> None:
        """
        사용자 세션을 삭제합니다.
        
        Args:
            user_id: 사용자 ID
        """
        if user_id in self.sessions:
            del self.sessions[user_id]
"""
로깅 유틸리티
"""
import logging
import sys
from typing import Optional

from .config import get_settings

def setup_logger(name: Optional[str] = None) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.
    
    Args:
        name: 로거 이름 (선택 사항)
        
    Returns:
        logging.Logger: 설정된 로거 인스턴스
    """
    settings = get_settings()
    logger_name = name or "slackbot"
    logger = logging.getLogger(logger_name)
    
    # 로그 레벨 설정
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 이미 핸들러가 설정되어 있는 경우 추가 설정 생략
    if logger.handlers:
        return logger
    
    # 콘솔 핸들러 설정
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger
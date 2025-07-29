"""
슬랙봇 FastAPI 애플리케이션 진입점
"""
import logging
import uvicorn
from fastapi import FastAPI, Query, Depends
from starlette.middleware.cors import CORSMiddleware

from controllers import slack_controller, mcp_controller
from utils.logger import setup_logger
from utils.config import get_settings
from services.slack_service import SlackService

# 로거 설정
logger = setup_logger("slackbot")

# FastAPI 애플리케이션 생성
app = FastAPI(title="Slack Bot API")

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(slack_controller.router, tags=["slack"])
app.include_router(mcp_controller.router, tags=["mcp"])



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
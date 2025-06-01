# 서버의 시작점

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.controllers import fms_controller
# from services.fms_service import FmsService

app = FastAPI()

# fms_service = FmsService()
app.include_router(fms_controller.router)

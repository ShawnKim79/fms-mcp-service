# 서버의 시작점

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from controllers import fms_controller
from services.fms_service import FmsService

app = FastAPI()
app.include_router(fms_controller.router)

fms_service = FmsService()

@app.on_event("startup")
async def startup_event():
    await fms_service.connect_db()

@app.on_event("shutdown")
async def shutdown_event():
    await fms_service.close_db()

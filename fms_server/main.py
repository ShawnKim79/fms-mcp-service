# 서버의 시작점

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from controllers import fms_controller

app = FastAPI()
app.include_router(fms_controller.router)

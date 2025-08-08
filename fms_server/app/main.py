# 서버의 시작점

import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from controllers import route_controller
from controllers import passenger_controller

app = FastAPI()

app.include_router(route_controller.router)
app.include_router(passenger_controller.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
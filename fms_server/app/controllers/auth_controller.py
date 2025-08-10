from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from config.database import get_db_session
from services.auth_service import AuthService
from controllers.dto.request_dto import RequestToken

router = APIRouter(prefix="/fms/auth")

def get_auth_service(db_session: Session = Depends(get_db_session)):
    return AuthService(session=db_session)

@router.post("/token")
async def login_for_access_token(request_token: RequestToken, auth_service: AuthService = Depends(get_auth_service)):
    
    user = auth_service.authenticate_user(request_token.nickname, request_token.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.nickname}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

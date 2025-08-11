from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from uuid import UUID

from config.database import get_db_session
from services.auth_service import AuthService

from domains.passenger import Passenger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db_session: Session = Depends(get_db_session)) -> Passenger:
    auth_service = AuthService(session=db_session)
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = auth_service.decode_access_token(token)
        
        nickname: str = payload.get("sub")
        
        if nickname is None:
            raise credentials_exception
        
    except (JWTError, ValueError):
        raise credentials_exception

    user = auth_service.get_passenger_by_nickname(nickname=nickname)
    if user is None:
        raise credentials_exception
    return Passenger.model_validate(user)

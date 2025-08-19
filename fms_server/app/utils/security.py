from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from services.auth_service import AuthService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    """Decode and validate a Bearer token, returning the JWT payload.

    DB 접근을 하지 않습니다. 호출자는 payload["sub"] 등 식별자를 이용해
    필요한 사용자 조회를 별도의 서비스로 수행해야 합니다.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = AuthService(session=None).decode_access_token(token)  # session 미사용 경로
        if not payload:
            raise credentials_exception
        sub = payload.get("sub")
        if not sub:
            raise credentials_exception
        return payload
    except (JWTError, ValueError):
        raise credentials_exception

# Deprecated: 남겨두되 내부적으로 토큰만 검증 후 401을 반환.
# 컨트롤러에서는 get_token_payload와 PassengerService를 사용해 사용자 로딩 권장.
def get_current_user_payload(token: str = Depends(oauth2_scheme)) -> dict:
    return get_token_payload(token)

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from sqlalchemy.orm import Session
from models.model import PassengerDB

from domains.passenger import Passenger

class AuthService:
    SECRET_KEY = "your-secret-key"  # 실제 환경에서는 환경 변수 등으로 관리해야 합니다.
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def __init__(self, session: Session):
        self.session = session
        

    def verify_password(self, plain_password, hashed_password):
        return pbkdf2_sha256.verify(plain_password, hashed_password)

    def authenticate_user(self, nickname: str, password: str) -> Optional[PassengerDB]:
        user = self.session.query(PassengerDB).filter(PassengerDB.nickname == nickname).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.password):
            return None
        
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

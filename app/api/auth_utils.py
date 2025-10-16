# app/api/auth_utils.py
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

def create_access_token(data: dict, minutes: int = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=minutes or int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        os.getenv("JWT_SECRET", "change_me"),
        algorithm=os.getenv("JWT_ALG", "HS256"),
    )

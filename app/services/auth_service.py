import os, datetime
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.repo import users_repo

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(p: str) -> str:
    return pwd.hash(p)

def verify_password(p: str, hashed: str) -> bool:
    return pwd.verify(p, hashed)

def create_user(db: Session, nombre: str, email: str, password: str, rol: str):
    hashed = hash_password(password)
    return users_repo.create(db, nombre=nombre, email=email, hashed_password=hashed, rol=rol)

def authenticate(db: Session, email: str, password: str):
    u = users_repo.get_by_email(db, email)
    if not u or not verify_password(password, u.hashed_password):
        return None
    return u

def create_access_token(user_id: int, role: str):
    now = datetime.datetime.utcnow()
    payload = {"sub": str(user_id), "role": role, "iat": now, "exp": now + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

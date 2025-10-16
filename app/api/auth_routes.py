# app/api/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import logging, os

# IMPORT CORRECTO: get_db vive en app/repo/db.py
from ..repo.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
log = logging.getLogger("auth")
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
DEBUG = os.getenv("DEBUG", "0") == "1"  # puedes activar con DEBUG=1 en compose

def create_access_token(sub: str, uid: int, rol: str) -> str:
    minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    payload = {
        "sub": sub,
        "uid": uid,
        "rol": rol,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
    }
    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET", "change_me"),
        algorithm=os.getenv("JWT_ALG", "HS256"),
    )

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginJSON(BaseModel):
    email: EmailStr
    password: str

def _get_user_by_email(db: Session, email: str):
    # mappings() -> dict-like; evita errores de atributo
    return db.execute(
        text("SELECT id, nombre, email, hashed_password, rol FROM usuarios WHERE email = :e"),
        {"e": email},
    ).mappings().first()

def _authenticate(db: Session, email: str, password: str):
    user = _get_user_by_email(db, email)
    if not user:
        return None
    try:
        ok = pwd_ctx.verify(password, user["hashed_password"])
    except Exception as e:
        # si alguna lib de bcrypt molestara, lo verás en logs
        log.exception("bcrypt verify failed for %s", email)
        raise
    if not ok:
        return None
    token = create_access_token(sub=user["email"], uid=user["id"], rol=user["rol"])
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login_form(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    try:
        email = (form.username or "").strip().lower()
        if not email:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="username requerido")
        auth = _authenticate(db, email, form.password)
        if not auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        return auth
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Login (form) error para %s", form.username)
        detail = f"{type(e).__name__}: {e}" if DEBUG else "Internal Server Error"
        raise HTTPException(status_code=500, detail=detail)

@router.post("/login_json", response_model=Token)
def login_json(body: LoginJSON, db: Session = Depends(get_db)):
    try:
        email = body.email.strip().lower()
        auth = _authenticate(db, email, body.password)
        if not auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
        return auth
    except HTTPException:
        raise
    except Exception as e:
        log.exception("Login (json) error para %s", body.email)
        detail = f"{type(e).__name__}: {e}" if DEBUG else "Internal Server Error"
        raise HTTPException(status_code=500, detail=detail)

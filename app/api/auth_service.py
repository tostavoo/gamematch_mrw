# app/api/auth_service.py
from sqlalchemy.orm import Session
from .repo import get_user_by_email
from .auth_utils import verify_password, create_access_token

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    token = create_access_token({"sub": user["email"], "uid": user["id"], "rol": user["rol"]})
    return {"access_token": token, "token_type": "bearer"}

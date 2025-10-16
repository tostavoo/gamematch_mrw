# app/api/repo.py
from typing import Optional
from sqlalchemy import text

def get_user_by_email(db, email: str) -> Optional[dict]:
    row = db.execute(
        text("SELECT id, nombre, email, hashed_password, rol FROM usuarios WHERE email=:e"),
        {"e": email}
    ).fetchone()
    if not row:
        return None
    return dict(row._mapping)

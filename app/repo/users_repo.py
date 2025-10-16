from sqlalchemy.orm import Session
from sqlalchemy import select
from app.domain.models import Usuario

def get_by_email(db: Session, email: str):
    return db.execute(select(Usuario).where(Usuario.email == email)).scalar_one_or_none()

def create(db: Session, nombre: str, email: str, hashed_password: str, rol: str):
    u = Usuario(nombre=nombre, email=email, hashed_password=hashed_password, rol=rol)
    db.add(u); db.commit(); db.refresh(u)
    return u

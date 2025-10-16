from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.domain.models import Interaccion, Juego

def add_interaction(db: Session, usuario_id: int, juego_id: int, liked: bool | None, rating: int | None):
    it = Interaccion(usuario_id=usuario_id, juego_id=juego_id, liked=liked, rating=rating, clicked=True)
    db.add(it); db.commit(); db.refresh(it)
    return it

def user_history(db: Session, user_id: int):
    return list(db.execute(select(Interaccion).where(Interaccion.usuario_id == user_id).order_by(Interaccion.ts.desc())).scalars())

def user_metrics(db: Session, user_id: int):
    total = db.execute(select(func.count()).select_from(Interaccion).where(Interaccion.usuario_id==user_id)).scalar()
    likes = db.execute(select(func.count()).select_from(Interaccion).where(Interaccion.usuario_id==user_id, Interaccion.liked==True)).scalar()
    clicks = db.execute(select(func.count()).select_from(Interaccion).where(Interaccion.usuario_id==user_id, Interaccion.clicked==True)).scalar()
    return {"total": int(total or 0), "likes": int(likes or 0), "clicks": int(clicks or 0)}

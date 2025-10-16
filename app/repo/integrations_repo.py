# app/repo/integrations_repo.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.domain.models import Juego
from app.repo.games_repo import get_or_create_by_title
from app.domain.models import Usuario
from app.domain.models import Juego as Game
from app.domain.models import Interaccion
from sqlalchemy import insert
from sqlalchemy.dialects.mysql import insert as mysql_insert

from sqlalchemy import Table, Column, Integer, Float, MetaData

# Acceso a la tabla user_game_stats sin ORM completo (rápido)
metadata = MetaData()
user_game_stats = Table(
    "user_game_stats", metadata,
    Column("user_id", Integer, primary_key=True),
    Column("game_id", Integer, primary_key=True),
    Column("playtime_hours", Float),
)

def upsert_user_hours(db: Session, user_id: int, game_id: int, hours: float):
    stmt = mysql_insert(user_game_stats).values(
        user_id=user_id, game_id=game_id, playtime_hours=hours
    )
    ondup = stmt.on_duplicate_key_update(playtime_hours=hours)
    db.execute(ondup)
    db.commit()

def get_or_create_game_by_title(db: Session, title: str, generos: str = "", tags: str = "", plataforma: str = "PC") -> Juego:
    return get_or_create_by_title(db, title, generos, tags, plataforma)

# app/repo/integrations_repo.py
from sqlalchemy import text

def get_user_hours_map(db, user_id: int) -> dict[int, float]:
    rows = db.execute(
        text("SELECT game_id, playtime_hours FROM user_game_stats WHERE user_id = :uid"),
        {"uid": user_id},
    ).all()
    return {int(gid): float(h or 0.0) for gid, h in rows}

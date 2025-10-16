from sqlalchemy.orm import Session
from sqlalchemy import select
from app.domain.models import Juego
from sqlalchemy.orm import Session
from app.domain.models import Juego
import csv, os

def list_all(db: Session):
    return list(db.execute(select(Juego).order_by(Juego.id)).scalars())

def create(db: Session, titulo: str, generos: str, tags: str, plataforma: str):
    g = Juego(titulo=titulo, generos=generos, tags=tags, plataforma=plataforma)
    db.add(g); db.commit(); db.refresh(g)
    return g

def seed_from_csv(db: Session, csv_path: str):
    if not os.path.exists(csv_path):
        return 0
    added = 0
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            g = Juego(
                titulo=row.get("titulo") or row.get("name") or "Juego",
                generos=row.get("generos",""),
                tags=row.get("tags",""),
                plataforma=row.get("plataforma","PC")
            )
            db.add(g); added += 1
    db.commit()
    return added

from sqlalchemy import select
from app.domain.models import Juego

def get_by_title(db, titulo: str) -> Juego | None:
    return db.execute(select(Juego).where(Juego.titulo == titulo)).scalar_one_or_none()

def get_or_create_by_title(
    db: Session,
    titulo: str,
    generos: str = "",
    tags: str = "",
    plataforma: str = "PC",
) -> Juego:
    """
    Devuelve un juego por título si existe (aunque haya duplicados, toma el más antiguo),
    o lo crea en caso contrario. Además, si el existente tiene campos vacíos, los completa.
    Esto evita MultipleResultsFound cuando ya existen duplicados en la tabla.
    """
    titulo = (titulo or "").strip()
    plataforma = (plataforma or "PC")[:50]
    generos = (generos or "").strip()
    tags = (tags or "").strip()

    # Tolerante: toma el primero (más antiguo) si hay varios
    q = db.query(Juego).filter(Juego.titulo == titulo).order_by(Juego.id.asc())
    existing = q.first()

    if existing:
        changed = False
        if generos and not (existing.generos or "").strip():
            existing.generos = generos
            changed = True
        if tags and not (existing.tags or "").strip():
            existing.tags = tags
            changed = True
        if plataforma and not (existing.plataforma or "").strip():
            existing.plataforma = plataforma
            changed = True
        if changed:
            db.commit()
            db.refresh(existing)
        return existing

    # Crear uno nuevo
    game = Juego(
        titulo=titulo,
        generos=generos,
        tags=tags,
        plataforma=plataforma,
    )
    db.add(game)
    db.commit()
    db.refresh(game)
    return game

# app/services/recommend_service.py
from __future__ import annotations

from typing import List, Tuple, Dict
from collections import Counter
from math import sqrt

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Juego, Interaccion
from app.repo.integrations_repo import get_user_hours_map


# -----------------------------
# Helpers
# -----------------------------
def _tokenize(s: str) -> list[str]:
    """Convierte una cadena 'a;b, c' en tokens normalizados ['a','b','c']."""
    if not s:
        return []
    return [t.strip().lower() for t in s.replace(",", ";").split(";") if t.strip()]

def _norm_title(t: str) -> str:
    """Normaliza título para deduplicar (lower + espacios colapsados)."""
    return " ".join((t or "").strip().lower().split())

def _build_user_profile(db: Session, user_id: int) -> Counter:
    """
    Construye un perfil de usuario como bolsa de tokens (generos/tags) usando
    interacciones con like=True.
    """
    q = (
        select(Juego.generos, Juego.tags)
        .join(Interaccion, Interaccion.juego_id == Juego.id)
        .where(Interaccion.usuario_id == user_id, Interaccion.liked == True)  # noqa: E712
    )
    tokens: list[str] = []
    for (generos, tags) in db.execute(q).all():
        tokens += _tokenize(generos) + _tokenize(tags)
    return Counter(tokens)

def _cosine(profile: Counter, toks: set[str]) -> float:
    """Similitud coseno simple entre el perfil (Counter) y los tokens del juego."""
    if not profile or not toks:
        return 0.0
    dot = sum(profile[t] for t in toks if t in profile)
    norm_p = sqrt(sum(v * v for v in profile.values()))
    norm_g = sqrt(len(toks))
    return (dot / (norm_p * norm_g)) if (norm_p and norm_g) else 0.0


# -----------------------------
# Recomendador principal
# -----------------------------
def recommend_for_user(
    db: Session,
    user_id: int,
    top: int = 5,
    alpha: float = 0.70,  # peso del modelo por contenido (1 - alpha = peso de horas)
) -> List[Tuple[float, Juego]]:
    """
    Devuelve una lista [(score, Juego), ...] ordenada desc.
    - Base: contenido (coseno con perfil por tokens).
    - Mezcla: horas reales de Steam normalizadas (si existen).
    - Deduplica por título (conserva el mejor score por juego).
    """
    # Perfil por likes (bolsa de géneros/tags)
    profile = _build_user_profile(db, user_id)
    profile_tokens = set(profile.keys())

    # Evita recomendar juegos ya interactuados (like/ratings/clicks)
    interacted_ids = {
        r[0]
        for r in db.execute(
            select(Interaccion.juego_id).where(Interaccion.usuario_id == user_id)
        ).all()
    }

    # Candidatos: todos los juegos no interactuados
    games = list(db.execute(select(Juego)).scalars())
    candidates = [g for g in games if g.id not in interacted_ids]

    # Ranking base por contenido
    scored: List[Tuple[float, Juego]] = []
    for g in candidates:
        toks = set(_tokenize(g.generos) + _tokenize(g.tags))
        if profile_tokens:
            prob = _cosine(profile, toks)
        else:
            # Sin historial: prioriza juegos con más señales (géneros/tags)
            prob = min(len(toks) / 6.0, 1.0)
        scored.append((float(prob), g))

    # Mezcla con horas reales de Steam (si existen)
    hours_map = get_user_hours_map(db, user_id) or {}
    if hours_map:
        # Normalización simple por máximo (evita dividir por cero)
        max_h = max(hours_map.values()) or 1.0

        def hnorm(gid: int) -> float:
            # Normaliza horas [0..1] y limita por seguridad
            return min(1.0, (hours_map.get(gid, 0.0) / max_h))

        # Si el usuario no tiene perfil aún, apoyarse un poco más en horas
        effective_alpha = alpha if profile else 0.40

        scored = [
            (effective_alpha * p + (1.0 - effective_alpha) * hnorm(g.id), g)
            for p, g in scored
        ]

    # --- DEDUP por título: conserva el mejor score por juego ---
    best_by_title: Dict[str, Tuple[float, Juego]] = {}
    for prob, game in scored:
        key = _norm_title(game.titulo) or f"id:{game.id}"
        if key not in best_by_title or prob > best_by_title[key][0]:
            best_by_title[key] = (prob, game)

    final = sorted(best_by_title.values(), key=lambda x: x[0], reverse=True)
    return [(float(p), g) for p, g in final[:top]]

# app/api/agent.py
from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.repo.db import get_db
from app.repo import interactions_repo
from app.repo.agent_repo import load_agent_params, save_agent_params
from app.workers.train_models import EGreedyAgent

# Intentamos importar el recomendador desde services; si no existe, usamos el de ml
try:
    from app.services.recommend_service import recommend_for_user
except Exception:
    from app.ml.content_based import recommend_for_user  # fallback

router = APIRouter()


def _normalize_pool(scored: list[Any]) -> list[tuple[int, float]]:
    """
    Acepta diferentes formatos que pueda devolver tu recomendador y
    devuelve una lista [(game_id, score_float), ...]
    """
    pool: list[tuple[int, float]] = []
    for item in scored:
        # caso típico: (prob, game_obj)
        if isinstance(item, (tuple, list)) and len(item) == 2:
            prob, game = item
            gid = getattr(game, "id", None) or (game.get("id") if isinstance(game, dict) else None)
            if gid is not None:
                try:
                    pool.append((int(gid), float(prob)))
                except Exception:
                    continue
            continue

        # si viene como dict: {"id": ..., "probabilidad"/"prob": ...}
        if isinstance(item, dict):
            gid = item.get("id")
            prob = item.get("prob") or item.get("probabilidad")
            if gid is not None and prob is not None:
                try:
                    pool.append((int(gid), float(prob)))
                except Exception:
                    continue

    pool.sort(key=lambda x: x[1], reverse=True)
    return pool


# ---------- GET /agent/{user_id}/recommendations ----------
@router.get("/agent/{user_id}/recommendations")
def agent_recommendations(
    user_id: int,
    limit: int = Query(10, ge=1, le=50),
    agent_mode: bool = Query(True),
    alpha: float = Query(0.7, ge=0.0, le=1.0, description="Peso del contenido (0..1)"),
    db: Session = Depends(get_db),
):
    # 1) Ranking base del modelo (pedimos pool grande)
    try:
        scored = recommend_for_user(db, user_id=user_id, top=max(50, limit), alpha=alpha)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en recommend_for_user: {e}")

    base_pool = _normalize_pool(scored)
    if not base_pool:
        return []  # sin datos base

    # 2) Directo o con agente ε-greedy
    if not agent_mode:
        chosen = base_pool[:limit]
    else:
        params = load_agent_params(db, user_id)
        agent = EGreedyAgent(params)
        chosen = agent.choose_k(base_pool, k=limit)
        save_agent_params(db, user_id, agent.params)

    # 3) Respuesta
    return [{"id": gid, "score": float(score)} for (gid, score) in chosen]


# ---------- POST /agent/{user_id}/feedback ----------
class FeedbackIn(BaseModel):
    game_id: int
    like: bool | None = None
    rating: float | None = None
    clicked: bool | None = None

def feedback_to_reward(data: FeedbackIn) -> int:
    if data.like is True:
        return 1
    if data.rating is not None and data.rating >= 4:
        return 1
    if data.clicked is True:
        return 1
    return 0

@router.post("/agent/{user_id}/feedback")
def agent_feedback(
    user_id: int,
    payload: FeedbackIn,
    db: Session = Depends(get_db),
):
    # 1) Guarda la interacción
    interactions_repo.add_interaction(
        db,
        usuario_id=user_id,
        juego_id=payload.game_id,
        liked=payload.like,
        rating=int(payload.rating) if payload.rating is not None else None,
    )

    # 2) Actualiza estado del agente (ε)
    reward = feedback_to_reward(payload)
    params = load_agent_params(db, user_id)
    agent = EGreedyAgent(params)
    agent.update_on_feedback(reward)
    save_agent_params(db, user_id, agent.params)

    return {"ok": True, "epsilon": agent.params.epsilon}


# ---------- GET /agent/{user_id}/state ----------
@router.get("/agent/{user_id}/state")
def agent_state(user_id: int, db: Session = Depends(get_db)):
    params = load_agent_params(db, user_id)
    return {
        "user_id": user_id,
        "epsilon": params.epsilon,
        "decay": params.decay,
        "min_epsilon": params.min_epsilon,
        "pulls": params.pulls,
        "rewards": params.rewards,
    }

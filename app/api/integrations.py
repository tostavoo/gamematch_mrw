# app/api/integrations.py
import os
from typing import Optional, List

import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.repo.db import get_db
from app.repo.games_repo import get_or_create_by_title
from app.repo.integrations_repo import upsert_user_hours

router = APIRouter()

# -----------------------------
# Helpers
# -----------------------------
def _mask(v: Optional[str]) -> Optional[str]:
    """Enmascara una API key para debug."""
    if not v:
        return None
    return (v[:4] + "…" + v[-4:]) if len(v) > 8 else "set"


def _get_env(name: str) -> Optional[str]:
    """Lee variable de entorno; si no existe, intenta cargar .env (opcional)."""
    val = os.environ.get(name)
    if val:
        return val
    try:
        from dotenv import load_dotenv  # opcional
        load_dotenv()
        return os.environ.get(name)
    except Exception:
        return None


def _clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))


# -----------------------------
# Debug
# -----------------------------
@router.get("/integrations/debug/env")
def debug_env():
    """Devuelve si el proceso ve las variables (enmascaradas)."""
    return {
        "RAWG_API_KEY": _mask(_get_env("RAWG_API_KEY")),
        "STEAM_API_KEY": _mask(_get_env("STEAM_API_KEY")),
    }


# -----------------------------
# RAWG: sembrar catálogo
# -----------------------------
@router.get("/integrations/rawg/seed")
def rawg_seed(
    query: str = Query(..., min_length=2, description="Texto a buscar en RAWG"),
    page_size: int = Query(12, ge=1, le=40),
    api_key: Optional[str] = Query(None, description="(opcional) override de RAWG_API_KEY"),
    db: Session = Depends(get_db),
):
    rawg_key = api_key or _get_env("RAWG_API_KEY")
    if not rawg_key:
        raise HTTPException(400, "Falta RAWG_API_KEY en el backend")

    url = "https://api.rawg.io/api/games"
    params = {"key": rawg_key, "search": query, "page_size": page_size}
    headers = {
        "User-Agent": "GameMatchPlus/1.0 (educational)",
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        try:
            payload = resp.json()
        except Exception as e:
            snippet = (resp.text or "")[:500]
            raise HTTPException(status_code=502, detail=f"RAWG response not JSON: {e}; snippet={snippet}")

        results = payload.get("results", [])
        if not isinstance(results, list):
            raise HTTPException(status_code=502, detail=f"RAWG 'results' is not a list: {type(results)}")

        items: List[dict] = []
        inserted_or_found = 0

        for g in results:
            title = (g.get("name") or "").strip() or "Sin título"
            genres = ";".join([x.get("name") for x in (g.get("genres") or []) if x.get("name")])

            # Normaliza plataformas (evita overflow de VARCHAR(50))
            plats_list = [
                p["platform"]["name"]
                for p in (g.get("platforms") or [])
                if p.get("platform") and p["platform"].get("name")
            ]
            if not plats_list:
                plataforma = "PC"
            else:
                plataforma = ";".join(plats_list)
                if len(plataforma) > 50:
                    plataforma = plats_list[0][:50]  # fallback seguro

            try:
                game = get_or_create_by_title(db, title, genres, "", plataforma)
            except SQLAlchemyError as e:
                db.rollback()
                err = getattr(e, "orig", e)
                raise HTTPException(status_code=500, detail=f"DB error saving '{title}': {err}")

            inserted_or_found += 1
            items.append(
                {
                    "id": game.id,
                    "titulo": game.titulo,
                    "generos": game.generos,
                    "plataforma": game.plataforma,
                }
            )

        return {"inserted_or_found": inserted_or_found, "items": items}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"RAWG request error: {e}")


# -----------------------------
# Steam: sincronizar horas jugadas
# -----------------------------
@router.get("/integrations/steam/sync")
def steam_sync(
    user_id: int = Query(..., description="ID interno de tu usuario"),
    steamid: str = Query(..., description="steamid64 del usuario"),
    include_free: int = Query(1),
    api_key: Optional[str] = Query(None, description="(opcional) override de STEAM_API_KEY"),
    db: Session = Depends(get_db),
):
    steam_key = api_key or _get_env("STEAM_API_KEY")
    if not steam_key:
        raise HTTPException(400, "Falta STEAM_API_KEY en el backend")

    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": steam_key,
        "steamid": steamid,
        "include_appinfo": 1,
        "include_played_free_games": include_free,
        "format": "json",
    }

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json().get("response", {})
        games = data.get("games", []) or []
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Steam request error: {e}")
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Steam JSON error: {e}")

    synced = 0
    for g in games:
        name = (g.get("name") or f"SteamApp {g.get('appid')}").strip()
        hours = float((g.get("playtime_forever", 0) or 0) / 60.0)
        try:
            game = get_or_create_by_title(db, name, "", "", "PC")
            upsert_user_hours(db, user_id=user_id, game_id=game.id, hours=hours)
            synced += 1
        except SQLAlchemyError as e:
            db.rollback()
            err = getattr(e, "orig", e)
            raise HTTPException(status_code=500, detail=f"DB error upserting hours for '{name}': {err}")

    return {"synced": synced, "steam_games_found": len(games)}


# -----------------------------
# Steam: top por horas (verificación rápida)
# -----------------------------
@router.get("/integrations/steam/top")
def steam_top(
    user_id: int = Query(...),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        lim = _clamp(int(limit), 1, 100)
        # Algunos drivers MySQL no aceptan bind param en LIMIT: lo inyectamos saneado
        q = f"""
        SELECT j.id, j.titulo, ugs.playtime_hours
        FROM user_game_stats ugs
        JOIN juegos j ON j.id = ugs.game_id
        WHERE ugs.user_id = :uid
        ORDER BY ugs.playtime_hours DESC
        LIMIT {lim}
        """
        rows = db.execute(text(q), {"uid": user_id}).all()
        return [{"id": int(r[0]), "titulo": r[1], "horas": float(r[2] or 0.0)} for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"steam_top error: {e}")

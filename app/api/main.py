from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from dotenv import load_dotenv, find_dotenv
import os

from app.api import agent as agent_routes
from app.api import integrations as integrations_routes
from app.repo.db import get_db
from app.domain import schemas
from app.repo import games_repo, interactions_repo
from app.services import auth_service, recommend_service

# Cargar variables de entorno desde .env
load_dotenv(find_dotenv())

# -----------------------------
# App & Swagger (con Bearer)
# -----------------------------
app = FastAPI(title="GameMatch+ API (MySQL)", version="0.2.0")

# Routers
app.include_router(agent_routes.router, tags=["agent"])
app.include_router(integrations_routes.router, tags=["integrations"])

# Definimos esquema OAuth2 para que Swagger muestre "Authorize"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def custom_openapi():
    """
    Añade el esquema de seguridad Bearer a la documentación para que
    aparezca el botón 'Authorize' en Swagger UI.
    (No obliga a usar el token en los endpoints.)
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GameMatch+ API (MySQL)",
        version="0.2.0",
        description="Plataforma de recomendación y análisis de videojuegos",
        routes=app.routes,
    )
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# -----------------------------
# Health
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# AUTH
# -----------------------------
@app.post("/auth/register", response_model=schemas.UserOut, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    from app.repo import users_repo
    if users_repo.get_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    u = auth_service.create_user(db, user.nombre, user.email, user.password, user.rol)
    return u

@app.post("/auth/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    u = auth_service.authenticate(db, form.username, form.password)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    token = auth_service.create_access_token(u.id, u.rol)
    return {"access_token": token, "token_type": "bearer"}

# -----------------------------
# GAMES
# -----------------------------
@app.get("/games", response_model=list[schemas.GameOut])
def list_games(db: Session = Depends(get_db)):
    return games_repo.list_all(db)

@app.post("/games", response_model=schemas.GameOut, status_code=201)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    return games_repo.create(db, game.titulo, game.generos, game.tags, game.plataforma)

# -----------------------------
# SEED (carga CSV de /data/games.csv)
# -----------------------------
@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "games.csv")
    )
    added = games_repo.seed_from_csv(db, csv_path)
    return {"added": added}

# -----------------------------
# FEEDBACK
# -----------------------------
@app.post("/users/{user_id}/feedback")
def feedback(user_id: int, fb: schemas.FeedbackIn, db: Session = Depends(get_db)):
    if not fb.juego_id:
        raise HTTPException(status_code=400, detail="juego_id requerido")
    interactions_repo.add_interaction(
        db,
        usuario_id=user_id,
        juego_id=fb.juego_id,
        liked=fb.liked,
        rating=fb.rating,
    )
    return {"ok": True}

# -----------------------------
# METRICS
# -----------------------------
@app.get("/users/{user_id}/metrics")
def metrics(user_id: int, db: Session = Depends(get_db)):
    return interactions_repo.user_metrics(db, user_id)

# -----------------------------
# RECOMMENDATIONS (con 'probabilidad' y alpha)
# -----------------------------
@app.get("/users/{user_id}/recommendations")
def recommendations(
    user_id: int,
    top: int = 5,
    alpha: float = Query(0.7, ge=0.0, le=1.0, description="Peso del contenido (0..1)"),
    db: Session = Depends(get_db),
):
    scored = recommend_service.recommend_for_user(db, user_id=user_id, top=top, alpha=alpha)
    return [
        {
            "id": g.id,
            "titulo": g.titulo,
            "generos": g.generos or "",
            "tags": g.tags or "",
            "plataforma": g.plataforma or "PC",
            "probabilidad": round(prob, 3),
        }
        for prob, g in scored
    ]

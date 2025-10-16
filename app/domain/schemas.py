from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict
from typing import Optional

# -------- Usuarios --------
class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str
    rol: str = "jugador"  # 'jugador' | 'administrador'

class UserOut(BaseModel):
    id: int
    nombre: str
    email: EmailStr
    rol: str
    # Pydantic v2: permitir crear desde objetos ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# -------- Juegos --------
class GameCreate(BaseModel):
    titulo: str
    generos: str = ""
    tags: str = ""
    plataforma: str = "PC"

class GameOut(BaseModel):
    id: int
    titulo: str
    generos: str
    tags: str
    plataforma: str
    model_config = ConfigDict(from_attributes=True)

# -------- Feedback --------
class FeedbackIn(BaseModel):
    juego_id: int
    liked: Optional[bool] = None
    rating: Optional[int] = None

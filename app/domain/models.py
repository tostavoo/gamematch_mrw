from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime, func

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(32), default="jugador")  # 'jugador' | 'administrador'

class Juego(Base):
    __tablename__ = "juegos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    generos: Mapped[str] = mapped_column(Text, default="")
    tags: Mapped[str] = mapped_column(Text, default="")
    plataforma: Mapped[str] = mapped_column(String(50), default="PC")

class Interaccion(Base):
    __tablename__ = "interacciones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    juego_id: Mapped[int] = mapped_column(ForeignKey("juegos.id"), nullable=False)
    rating: Mapped[int | None] = mapped_column(Integer, nullable=True)
    liked: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    clicked: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    ts: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

# en app/domain/models.py (al final del archivo)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Float, ForeignKey, DateTime, func

class AgentState(Base):
    __tablename__ = "agent_state"
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    epsilon: Mapped[float] = mapped_column(Float, default=0.20, nullable=False)
    decay: Mapped[float] = mapped_column(Float, default=0.995, nullable=False)
    min_epsilon: Mapped[float] = mapped_column(Float, default=0.05, nullable=False)
    pulls: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rewards: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserGameStats(Base):
    __tablename__ = "user_game_stats"
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("juegos.id"), primary_key=True)
    playtime_hours: Mapped[float] = mapped_column(Float, default=0.0)
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
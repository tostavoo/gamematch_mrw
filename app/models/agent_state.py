# app/models/agent_state.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
# 👇 usa tu Base ya existente (ajusta el import si tu Base está en otro módulo)
from app.domain.models import Base


class AgentState(Base):
    __tablename__ = "agent_state"
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    epsilon = Column(Float, default=0.20, nullable=False)
    decay = Column(Float, default=0.995, nullable=False)
    min_epsilon = Column(Float, default=0.05, nullable=False)
    pulls = Column(Integer, default=0, nullable=False)
    rewards = Column(Integer, default=0, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

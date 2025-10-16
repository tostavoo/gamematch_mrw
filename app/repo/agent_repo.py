# app/repo/agent_repo.py
from sqlalchemy.orm import Session
from app.domain.models import AgentState
from app.workers.train_models import AgentParams

__all__ = ["load_agent_params", "save_agent_params"]

def load_agent_params(db: Session, user_id: int) -> AgentParams:
    row = db.get(AgentState, user_id)
    if row is None:
        return AgentParams()
    return AgentParams(
        epsilon=row.epsilon,
        decay=row.decay,
        min_epsilon=row.min_epsilon,
        pulls=row.pulls,
        rewards=row.rewards,
    )

def save_agent_params(db: Session, user_id: int, params: AgentParams) -> None:
    row = db.get(AgentState, user_id)
    if row is None:
        row = AgentState(user_id=user_id)
    row.epsilon = params.epsilon
    row.decay = params.decay
    row.min_epsilon = params.min_epsilon
    row.pulls = params.pulls
    row.rewards = params.rewards
    db.merge(row)
    db.commit()

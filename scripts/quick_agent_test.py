# scripts/quick_agent_test.py
import random
from app.workers.train_models import EGreedyAgent, AgentParams

# Recomendaciones simuladas (id_juego, score)
base_recs = [(1, 0.92), (2, 0.88), (3, 0.71), (4, 0.65), (5, 0.60)]

# Semilla para que el resultado sea reproducible (opcional)
random.seed(42)

agent = EGreedyAgent(AgentParams(epsilon=0.3))

print("ε inicial:", round(agent.params.epsilon, 4))
top3 = agent.choose_k(base_recs, k=3)
print("Top 3 con agente:", top3)

# Simula un buen feedback (like/click = 1)
agent.update_on_feedback(1)
print("ε tras buen feedback:", round(agent.params.epsilon, 4))

# app/workers/train_models.py
import random
from dataclasses import dataclass

@dataclass
class AgentParams:
    epsilon: float = 0.20
    decay: float = 0.995
    min_epsilon: float = 0.05
    pulls: int = 0
    rewards: int = 0

class EGreedyAgent:
    """
    Agente ε-greedy para mezclar exploración y explotación.
    Uso:
      - init con parámetros (o cargados de BD)
      - choose_k(recommendations, k) para obtener K items
      - update_on_feedback(reward) tras feedback del usuario (1/0)
    """
    def __init__(self, params: AgentParams | None = None):
        self.params = params or AgentParams()

    def _maybe_decay(self):
        # Decaimiento suave tras cada decisión
        self.params.epsilon = max(self.params.min_epsilon, self.params.epsilon * self.params.decay)
        self.params.pulls += 1

    def choose_one(self, recommendations: list[tuple[int, float]], already=None):
        """
        recommendations: lista [(game_id, score), ...]
        already: set de ids ya elegidos (para no repetir)
        """
        already = already or set()
        pool = [(gid, s) for gid, s in recommendations if gid not in already]
        if not pool:
            return None

        r = random.random()
        if r < self.params.epsilon:
            # Explorar: aleatorio del pool completo (o podrías limitar a top-N para ser "exploración informada")
            choice = random.choice(pool)
        else:
            # Explotar: mayor score
            choice = max(pool, key=lambda x: x[1])

        self._maybe_decay()
        return choice

    def choose_k(self, recommendations: list[tuple[int, float]], k: int = 10):
        """
        Devuelve hasta k items sin repetir, combinando exploración/explotación.
        """
        chosen = []
        used = set()
        for _ in range(min(k, len(recommendations))):
            c = self.choose_one(recommendations, already=used)
            if not c:
                break
            chosen.append(c)
            used.add(c[0])
        return chosen

    def update_on_feedback(self, reward: int):
        """
        reward: 1 (positivo: like/click/alta calificación) o 0 (negativo).
        Ajuste de epsilon en línea:
          - Recompensa alta -> menor exploración (confianza ↑)
          - Recompensa baja -> ligeramente más exploración
        """
        if reward not in (0, 1):
            return
        self.params.rewards += reward
        if reward == 1:
            # reducir epsilon un poco extra
            self.params.epsilon = max(self.params.min_epsilon, self.params.epsilon * 0.99)
        else:
            # subir levemente para explorar más
            self.params.epsilon = min(0.8, self.params.epsilon * 1.01)

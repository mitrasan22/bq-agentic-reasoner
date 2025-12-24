from typing import Dict
from bq_agentic_reasoner.config import load_config


class LearningWeightUpdater:
    """
    Adjusts optimization weights based on feedback signals.
    """

    def __init__(self):
        self.config = load_config()

    def update_weights(
        self,
        *,
        signals: Dict[str, float],
        learning_rate: float = 0.1,
    ) -> Dict[str, float]:
        """
        Apply learning update to optimization weights.
        """

        weights = self.config["learning_weights"].get(
            "optimization_weights", {}
        )

        updated = weights.copy()

        for opt, acceptance_ratio in signals.items():
            base = weights.get(opt, 1.0)

            # Positive feedback → increase weight
            delta = (acceptance_ratio - 0.5) * learning_rate
            updated[opt] = round(max(0.1, base + delta), 2)

        return updated

from typing import List, Dict
from collections import defaultdict


class LearningSignalExtractor:
    """
    Extracts learning signals from rewrite feedback.
    """

    def extract(self, feedback_docs: List[Dict]) -> Dict[str, float]:
        """
        Convert feedback history into acceptance ratios
        per optimization type.
        """

        stats = defaultdict(lambda: {"accepted": 0, "total": 0})

        for doc in feedback_docs:
            opt = doc.get("optimization_type")
            if not opt:
                continue

            stats[opt]["total"] += 1
            if doc.get("accepted"):
                stats[opt]["accepted"] += 1

        signals = {}
        for opt, values in stats.items():
            if values["total"] > 0:
                signals[opt] = values["accepted"] / values["total"]

        return signals

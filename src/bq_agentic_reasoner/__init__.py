"""
bq_agentic_reasoner

BigQuery Agentic Reasoner – Public API surface.

This package provides:
- Realtime BigQuery job analysis
- Async agentic enrichment
- Safe query optimization
- History & learning support

Only objects imported here are considered STABLE.
Internal modules may change without notice.
"""

# =========================
# Core orchestration
# =========================

from bq_agentic_reasoner.backend.orchestrator import Orchestrator

# =========================
# Pipelines (advanced users)
# =========================

from bq_agentic_reasoner.backend.pipeline_realtime import RealtimePipeline
from bq_agentic_reasoner.backend.pipeline_enrichment import EnrichmentPipeline

# =========================
# Models (read-only access)
# =========================

from bq_agentic_reasoner.models.public import (
    RealtimeResult,
    RunResult,
    LLMRecommendation,
)

from bq_agentic_reasoner.models.rewrite import (
    RewriteCandidate,
    RewriteSet,
)

# =========================
# Configuration
# =========================

from bq_agentic_reasoner.config.loader import load_config

# =========================
# Version
# =========================

__version__ = "0.1.0"

# =========================
# Public API contract
# =========================

__all__ = [
    # Core
    "Orchestrator",

    # Pipelines
    "RealtimePipeline",
    "EnrichmentPipeline",

    # Models
    "RealtimeResult",
    "RunResult",
    "LLMRecommendation",
    "RewriteCandidate",
    "RewriteSet",

    # Config
    "load_config",
]

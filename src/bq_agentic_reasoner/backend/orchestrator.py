from bq_agentic_reasoner.backend.event_processor import EventProcessor
from bq_agentic_reasoner.backend.pipeline_realtime import RealtimePipeline
from bq_agentic_reasoner.backend.pipeline_enrichment import EnrichmentPipeline
from bq_agentic_reasoner.backend.scheduler import AsyncScheduler
from bq_agentic_reasoner.history.store import record_run
import logging


class Orchestrator:
    """
    Central coordinator.
    Safe for Cloud Functions (no side effects at import time).
    """

    def __init__(self):
        # ✅ NEVER create heavy / secret-dependent objects here
        self._processor = None
        self._realtime = None
        self._enrichment = None
        self._scheduler = None

    # ---------- lazy getters ----------

    def _get_processor(self) -> EventProcessor:
        if self._processor is None:
            self._processor = EventProcessor()
        return self._processor

    def _get_realtime(self) -> RealtimePipeline:
        if self._realtime is None:
            self._realtime = RealtimePipeline()
        return self._realtime

    def _get_enrichment(self) -> EnrichmentPipeline:
        if self._enrichment is None:
            self._enrichment = EnrichmentPipeline()
        return self._enrichment

    def _get_scheduler(self) -> AsyncScheduler:
        if self._scheduler is None:
            self._scheduler = AsyncScheduler()
        return self._scheduler

    # ---------- public API ----------

    def handle_event(self, raw_event: dict) -> None:
        """
        Entry point called by Cloud Function.
        """
        processor = self._get_processor()
        realtime = self._get_realtime()
        scheduler = self._get_scheduler()

        event = processor.process(raw_event)
        logging.error(f"PIPELINE REALTIME EVENT: {event}")

        realtime_result = realtime.run(event)
        record_run(realtime_result)

        # enrichment happens async / later
        scheduler.run(
            self._run_enrichment,
            event,
            realtime_result,
        )

    def _run_enrichment(self, event: dict, realtime_result) -> None:
        enrichment = self._get_enrichment()
        enriched = enrichment.run(event, realtime_result)
        record_run(enriched)

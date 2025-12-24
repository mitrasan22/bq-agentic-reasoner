from bq_agentic_reasoner.backend.event_processor import EventProcessor
from bq_agentic_reasoner.backend.pipeline_realtime import RealtimePipeline
from bq_agentic_reasoner.backend.pipeline_enrichment import EnrichmentPipeline
from bq_agentic_reasoner.backend.scheduler import AsyncScheduler
from bq_agentic_reasoner.history.store import record_run


class Orchestrator:
    """
    Central coordinator.
    Called by Cloud Functions or simulators.
    """

    def __init__(self):
        self.processor = EventProcessor()
        self.realtime = RealtimePipeline()
        self.enrichment = EnrichmentPipeline()
        self.scheduler = AsyncScheduler()

    def handle_event(self, raw_event: dict) -> None:
        event = self.processor.process(raw_event)
        realtime_result = self.realtime.run(event)
        record_run(realtime_result)
        self.scheduler.run(
            self._run_enrichment,
            event,
            realtime_result,
        )

    def _run_enrichment(self, event: dict, realtime_result) -> None:
        enriched = self.enrichment.run(event, realtime_result)
        record_run(enriched)

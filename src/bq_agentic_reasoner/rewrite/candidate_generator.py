import re
import json
import logging
from typing import List
from bq_agentic_reasoner.models.rewrite import RewriteCandidate
from bq_agentic_reasoner.models.confidence import RewriteConfidence
from bq_agentic_reasoner.llm.hf_client import HuggingFaceClient
from bq_agentic_reasoner.rewrite.validator import SQLValidator
from bq_agentic_reasoner.rewrite.comparator import CostComparator

class CandidateGenerator:
    def __init__(self):
        self.client = HuggingFaceClient()
        self.validator = SQLValidator()
        self.cost_comparator = CostComparator()

    def generate(self, *, sql: str, metadata: dict, ml_context: any = None) -> List[RewriteCandidate]:
        if not sql:
            return []

        prompt = self._build_agentic_prompt(sql, metadata, ml_context)
        response_text = self.client.generate(prompt)
        return self._process_suggestions(response_text, metadata)

    def _build_agentic_prompt(self, sql: str, metadata: dict, ml_context: any) -> str:
        base_cost_gb = metadata.get("estimated_bytes", 0) / (1024 ** 3)
        
        return f"""
        You are a Senior BigQuery Architect and ML Engineer.
        Task: Analyze the input and provide two distinct, optimized SQL rewrites in JSON format.

        --- INPUT DATA ---
        SQL QUERY: 
        {sql}

        METADATA:
        - Estimated Scan: {base_cost_gb:.4f} GB
        - Resource Stats: {metadata}
        
        MODEL PERFORMANCE (if BQML):
        {ml_context if ml_context else "Standard SQL Query (No ML Context provided)"}

        --- OPTIMIZATION GUIDELINES ---
        1. ADVANCED SQL: 
           - Replace 'SELECT *' with specific schema-aware columns.
           - Implement Partition Pruning (e.g., add WHERE filters on _PARTITIONTIME or date columns).
           - Optimize JOINs (suggest INNER instead of CROSS, or use persistent UDFs).
        
        2. BQML SPECIALIZATION:
           - If accuracy/precision is low: Suggest hyperparameter tuning (L1_REG, L2_REG).
           - If training is slow: Suggest EARLY_STOP=TRUE or decreasing MAX_ITERATIONS.
           - If data is imbalanced: Suggest 'AUTO_CLASS_WEIGHTS=TRUE'.
           - For COVID/Time-Series: Suggest 'DATA_SPLIT_METHOD="SEQ"' if training on temporal data.

        --- OUTPUT REQUIREMENTS ---
        Return ONLY a JSON array containing two objects. No conversational text.
        Format:
        [
          {{
            "query": "The fully executable optimized SQL string",
            "explanation": "Detailed technical reasoning for the change",
            "predicted_gb_pct": 0.0
          }}
        ]
        """

    def _process_suggestions(self, text: str, metadata: dict) -> List[RewriteCandidate]:
        candidates = []
        try:
            json_match = re.search(r'\[\s*\{.*\}\s*\]', text, re.DOTALL)
            if not json_match:
                return []
            
            suggestions = json.loads(json_match.group(0))
            original_gb = metadata.get("estimated_bytes", 0) / (1024 ** 3)

            for item in suggestions:
                opt_query = item.get("query")
                
                if opt_query and self.validator.validate(opt_query):
                    cost_info = self.cost_comparator.estimate(
                        original_gb=original_gb,
                        optimized_gb=original_gb * item.get("predicted_gb_pct", 1.0)
                    )

                    candidates.append(RewriteCandidate(
                        optimized_query=opt_query,
                        optimizations_applied=["AGENTIC_LLM_REWRITE"],
                        explanation=item.get("explanation"),
                        cost_comparison=cost_info,
                        confidence=RewriteConfidence(
                            score=0.9,
                            level="HIGH",
                            reasons=["LLM-reasoned optimization verified by static analysis"]
                        )
                    ))
        except Exception:
            return []

        return candidates
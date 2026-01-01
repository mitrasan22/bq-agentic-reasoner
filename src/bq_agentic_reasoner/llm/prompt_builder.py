from bq_agentic_reasoner.models.public import RealtimeResult


class PromptBuilder:
    """
    Builds safe, structured prompts for the LLM.
    """

    SYSTEM_PROMPT = """
You are a BigQuery performance and cost optimization expert.

Rules:
- You NEVER execute SQL
- You NEVER invent table or column names
- You ONLY analyze the provided SQL
- You must explain reasoning clearly
- You may suggest optimized SQL if safe
- If optimization is unclear, say so explicitly
"""

    def build_explanation_prompt(
        self,
        *,
        result: RealtimeResult,
        sql: str | None,
        ml_context: any = None,
    ) -> str:
        prompt = f"""
{self.SYSTEM_PROMPT}

Context:
- Job type: {result.job_type}
- Severity: {result.severity}
- Estimated scan cost (GB): {result.estimated_cost_gb}
- Risk level: {result.risk}
- Query intent: {result.intent}
- ML Evaluation Stats: {ml_context if ml_context else "N/A"}

Original SQL:
{sql if sql else "[NO SQL AVAILABLE]"}

Tasks:
1. Explain why this query is expensive or risky (if applicable)
2. If this is a BQML job, analyze the ML Evaluation Stats for model performance
3. Suggest concrete improvements
4. If possible, provide an optimized SQL version
5. If not possible, explain why
"""

        return prompt.strip()
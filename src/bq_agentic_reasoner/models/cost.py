from pydantic import BaseModel, Field


class CostComparison(BaseModel):
    """
    Estimated BigQuery scan cost impact.
    """

    original_estimated_gb: float = Field(ge=0)
    optimized_estimated_gb: float = Field(ge=0)

    estimated_savings_pct: float = Field(
        ge=0,
        le=100,
        description="Estimated percentage cost reduction",
    )

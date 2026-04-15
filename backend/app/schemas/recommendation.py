"""
Recommendation Pydantic schemas with detailed score breakdown.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RecommendationResponse(BaseModel):
    id: int
    user_id: int
    vacancy_id: int
    overall_score: float
    keyword_score: float = 0.0
    semantic_score: float = 0.0
    matched_skills: list[str] | None = None
    missing_skills: list[str] | None = None
    explanation: str | None = None
    strategy: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RecommendationWithVacancy(RecommendationResponse):
    """Recommendation response that includes the full vacancy details."""

    vacancy: "VacancyResponse"  # type: ignore  # Forward ref


class GenerateRecommendationsResponse(BaseModel):
    """Response for the generate endpoint."""

    strategy: str = Field(..., description="Strategy used for matching")
    generated_count: int = Field(..., description="Number of recommendations created")
    results: list[RecommendationWithVacancy] = Field(
        default_factory=list,
        description="Top-ranked recommendations with vacancy details",
    )


class StrategyInfo(BaseModel):
    """Metadata about an available matching strategy."""

    name: str
    description: str


class StrategiesResponse(BaseModel):
    """Response for GET /recommendations/strategies."""

    strategies: list[StrategyInfo]


# Avoid circular import
from app.schemas.vacancy import VacancyResponse  # noqa: E402

RecommendationWithVacancy.model_rebuild()

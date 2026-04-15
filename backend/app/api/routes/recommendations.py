"""
Recommendation routes v2.

Endpoints:
  POST /recommendations/generate  — Run matching with chosen strategy
  GET  /recommendations/me        — Get saved recommendations
  GET  /recommendations/me/{vacancy_id}  — Get single recommendation detail
  GET  /recommendations/strategies       — List available strategies
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.recommendation import (
    GenerateRecommendationsResponse,
    RecommendationWithVacancy,
    StrategiesResponse,
)
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post(
    "/generate",
    response_model=GenerateRecommendationsResponse,
)
async def generate_recommendations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    strategy: str = Query(
        "keyword",
        description="Matching strategy: keyword, tfidf, or embeddings",
    ),
    top_k: int = Query(20, ge=1, le=100, description="Number of results"),
):
    """
    Generate fresh recommendations using the specified matching strategy.

    - **keyword**: Fast, explainable skill matching with a controlled dictionary.
    - **tfidf**: TF-IDF + cosine similarity for broader vocabulary matching.
    - **embeddings**: Semantic matching using sentence-transformers (slower, deeper).

    Old recommendations for this user are replaced.
    """
    service = RecommendationService(db)
    try:
        results = await service.generate_recommendations(
            user_id=current_user.id, strategy=strategy, top_k=top_k
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    vacancy_results = _to_vacancy_responses(service, results)

    return GenerateRecommendationsResponse(
        strategy=strategy,
        generated_count=len(vacancy_results),
        results=vacancy_results,
    )


@router.get("/me", response_model=list[RecommendationWithVacancy])
async def get_my_recommendations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    limit: int = Query(20, ge=1, le=100),
):
    """Get the current user's saved recommendations."""
    service = RecommendationService(db)
    recs = await service.get_recommendations(user_id=current_user.id, limit=limit)
    return _to_vacancy_responses(service, recs)


@router.get("/me/{vacancy_id}", response_model=RecommendationWithVacancy)
async def get_recommendation_detail(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    vacancy_id: int = Path(..., gt=0),
):
    """Get detailed recommendation for a specific vacancy."""
    service = RecommendationService(db)
    rec = await service.get_recommendation_for_vacancy(current_user.id, vacancy_id)
    if not rec:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommendation found for this vacancy. Generate recommendations first.",
        )

    return _to_vacancy_response(service, rec)


@router.get("/strategies", response_model=StrategiesResponse)
async def list_available_strategies():
    """List all available matching strategies with descriptions."""
    return StrategiesResponse(strategies=RecommendationService.available_strategies())


# ── Internal helpers ──────────────────────────────────────────────

def _to_vacancy_responses(
    service: RecommendationService, recs: list
) -> list[RecommendationWithVacancy]:
    return [_to_vacancy_response(service, r) for r in recs]


def _to_vacancy_response(
    service: RecommendationService, rec
) -> RecommendationWithVacancy:
    return RecommendationWithVacancy(
        id=rec.id,
        user_id=rec.user_id,
        vacancy_id=rec.vacancy_id,
        overall_score=rec.overall_score,
        keyword_score=rec.keyword_score,
        semantic_score=rec.semantic_score,
        matched_skills=service.repo.skills_from_json(rec.matched_skills),
        missing_skills=service.repo.skills_from_json(rec.missing_skills),
        explanation=rec.explanation,
        strategy=rec.strategy,
        created_at=rec.created_at,
        updated_at=rec.updated_at,
        vacancy=rec.vacancy,  # type: ignore[arg-type]
    )

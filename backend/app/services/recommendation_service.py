"""
Recommendation service v2 — orchestrates the AI matching pipeline
with pluggable matching strategies.

This service:
  1. Fetches the user's latest resume
  2. Fetches all active vacancies
  3. Runs the AI matching engine with the chosen strategy
  4. Persists the results (with strategy metadata)
  5. Returns ranked recommendations with vacancy details
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.engine import RecommendationEngine
from app.ai.factory import list_strategies
from app.models.recommendation import Recommendation
from app.repositories.recommendation_repository import RecommendationRepository
from app.repositories.resume_repository import ResumeRepository
from app.repositories.vacancy_repository import VacancyRepository


class RecommendationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = RecommendationRepository(db)
        self.engine = RecommendationEngine()

    async def get_recommendations(
        self, user_id: int, limit: int = 20
    ) -> list[Recommendation]:
        """Return the top saved recommendations for a user."""
        return await self.repo.get_for_user(user_id, limit=limit)

    async def get_recommendation_for_vacancy(
        self, user_id: int, vacancy_id: int
    ) -> Recommendation | None:
        """Return a specific recommendation for a user-vacancy pair."""
        return await self.repo.get_for_user_and_vacancy(user_id, vacancy_id)

    async def generate_recommendations(
        self, user_id: int, strategy: str = "keyword", top_k: int = 20
    ) -> list[Recommendation]:
        """
        Run the full matching pipeline with the specified strategy.

        Steps:
          1. Get user's latest resume
          2. Fetch all active vacancies
          3. Run the AI matching engine with the chosen strategy
          4. Delete old recommendations for this user
          5. Persist new results with strategy metadata
          6. Return the top-K recommendations with vacancies eager-loaded

        Args:
            user_id:  Authenticated user ID.
            strategy: One of 'keyword', 'tfidf', 'embeddings'.
            top_k:    Number of top results to keep.

        Returns:
            List of Recommendation ORM objects (with vacancy eager-loaded).

        Raises:
            ValueError: If no resume or no vacancies exist.
        """
        # 1. Get user's latest resume
        resume_repo = ResumeRepository(self.db)
        resumes = await resume_repo.get_by_user(user_id)
        if not resumes:
            raise ValueError("No resume found. Please upload one first.")

        latest_resume = resumes[0]  # Ordered by uploaded_at desc
        resume_text = latest_resume.extracted_text
        if not resume_text or not resume_text.strip():
            raise ValueError("No text extracted from this resume.")

        # 2. Fetch all active vacancies
        vacancy_repo = VacancyRepository(self.db)
        vacancies = await vacancy_repo.get_active()
        if not vacancies:
            raise ValueError("No active vacancies in the system.")

        vacancy_dicts = [
            {
                "id": v.id,
                "title": v.title,
                "company": v.company,
                "description": v.description,
                "requirements": v.requirements,
            }
            for v in vacancies
        ]

        # 3. Run the AI matching engine
        results = self.engine.generate(
            resume_text=resume_text,
            vacancies=vacancy_dicts,
            top_k=top_k,
            strategy=strategy,
        )

        # 4. Delete old recommendations
        await self.repo.delete_for_user(user_id)

        # 5. Persist new results
        records = []
        for r in results:
            records.append({
                "user_id": user_id,
                "vacancy_id": r.vacancy_id,
                "overall_score": r.overall_score,
                "keyword_score": r.keyword_score,
                "semantic_score": r.semantic_score,
                "matched_skills": self.repo.skills_to_json(r.matched_skills),
                "missing_skills": self.repo.skills_to_json(r.missing_skills),
                "explanation": r.explanation,
                "strategy": strategy,
            })

        if records:
            await self.repo.bulk_create(records)

        # 6. Return with vacancies eager-loaded
        return await self.repo.get_for_user(user_id, limit=top_k)

    @staticmethod
    def available_strategies() -> list[dict[str, str]]:
        """Return metadata about available matching strategies."""
        return list_strategies()

"""
Recommendation repository.
"""

import json

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.recommendation import Recommendation
from app.repositories.base import BaseRepository


class RecommendationRepository(BaseRepository[Recommendation]):
    def __init__(self, db: AsyncSession):
        super().__init__(Recommendation, db)

    async def get_for_user(
        self, user_id: int, limit: int = 20
    ) -> list[Recommendation]:
        """Get top recommendations for a user, eagerly loading the vacancy."""
        stmt = (
            select(Recommendation)
            .options(selectinload(Recommendation.vacancy))  # type: ignore[arg-type]
            .where(Recommendation.user_id == user_id)
            .order_by(Recommendation.overall_score.desc())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_for_user_and_vacancy(
        self, user_id: int, vacancy_id: int
    ) -> Recommendation | None:
        """Get a specific recommendation for a user-vacancy pair."""
        stmt = (
            select(Recommendation)
            .options(selectinload(Recommendation.vacancy))  # type: ignore[arg-type]
            .where(
                Recommendation.user_id == user_id,
                Recommendation.vacancy_id == vacancy_id,
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_for_user(self, user_id: int) -> int:
        """Delete all existing recommendations for a user. Returns count."""
        stmt = delete(Recommendation).where(Recommendation.user_id == user_id)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount  # type: ignore[return-value]

    async def bulk_create(self, records: list[dict]) -> list[Recommendation]:
        """Insert multiple recommendation records in one transaction."""
        instances = [Recommendation(**data) for data in records]
        self.db.add_all(instances)
        await self.db.flush()
        for inst in instances:
            await self.db.refresh(inst)
        return instances

    @staticmethod
    def skills_to_json(skills: list[str] | None) -> str | None:
        """Serialize a list of skills to a JSON string for storage."""
        if not skills:
            return None
        return json.dumps(skills)

    @staticmethod
    def skills_from_json(raw: str | None) -> list[str] | None:
        """Deserialize a JSON string back to a list of skills."""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return None

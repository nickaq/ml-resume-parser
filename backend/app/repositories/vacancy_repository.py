"""
Vacancy repository.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vacancy import Vacancy
from app.repositories.base import BaseRepository


class VacancyRepository(BaseRepository[Vacancy]):
    def __init__(self, db: AsyncSession):
        super().__init__(Vacancy, db)

    async def get_active(self, skip: int = 0, limit: int = 100) -> list[Vacancy]:
        """Get only active vacancies."""
        stmt = (
            select(Vacancy)
            .where(Vacancy.is_active.is_(True))
            .order_by(Vacancy.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def search(self, query: str, skip: int = 0, limit: int = 50) -> list[Vacancy]:
        """Search vacancies by title, company, or description (case-insensitive)."""
        search_pattern = f"%{query.lower()}%"
        stmt = (
            select(Vacancy)
            .where(
                Vacancy.is_active.is_(True),
                (
                    Vacancy.title.ilike(search_pattern)
                    | Vacancy.company.ilike(search_pattern)
                    | Vacancy.description.ilike(search_pattern)
                ),
            )
            .order_by(Vacancy.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

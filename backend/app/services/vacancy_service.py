"""
Vacancy service — handles vacancy CRUD operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vacancy import Vacancy
from app.repositories.vacancy_repository import VacancyRepository
from app.utils.helpers import filter_none


class VacancyService:
    def __init__(self, db: AsyncSession):
        self.repo = VacancyRepository(db)

    async def create(self, **kwargs) -> Vacancy:
        return await self.repo.create(kwargs)

    async def get_by_id(self, vacancy_id: int) -> Vacancy | None:
        return await self.repo.get_by_id(vacancy_id)

    async def get_active(self, skip: int = 0, limit: int = 100) -> list[Vacancy]:
        return await self.repo.get_active(skip=skip, limit=limit)

    async def search(self, query: str, skip: int = 0, limit: int = 50) -> list[Vacancy]:
        """Search vacancies by text query."""
        return await self.repo.search(query, skip=skip, limit=limit)

    async def update(self, vacancy_id: int, data: dict) -> Vacancy | None:
        vacancy = await self.repo.get_by_id(vacancy_id)
        if not vacancy:
            return None
        return await self.repo.update(vacancy, filter_none(data))

    async def delete(self, vacancy_id: int) -> bool:
        vacancy = await self.repo.get_by_id(vacancy_id)
        if not vacancy:
            return False
        await self.repo.delete(vacancy)
        return True

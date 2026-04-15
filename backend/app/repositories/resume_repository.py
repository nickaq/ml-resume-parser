"""
Resume repository.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.repositories.base import BaseRepository


class ResumeRepository(BaseRepository[Resume]):
    def __init__(self, db: AsyncSession):
        super().__init__(Resume, db)

    async def get_by_user(self, user_id: int) -> list[Resume]:
        """Get all resumes belonging to a user, newest first."""
        stmt = (
            select(Resume)
            .where(Resume.user_id == user_id)
            .order_by(Resume.uploaded_at.desc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

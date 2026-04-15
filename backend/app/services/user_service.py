"""
User service — business logic for registration and authentication.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(
        self,
        email: str,
        password: str,
        full_name: str | None = None,
        role: UserRole = UserRole.USER,
    ) -> User:
        """Create a new user with a hashed password."""
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError(f"User with email '{email}' already exists")

        return await self.repo.create({
            "email": email,
            "hashed_password": hash_password(password),
            "full_name": full_name,
            "role": role.value,
        })

    async def authenticate(self, email: str, password: str) -> User | None:
        """Return user if credentials are valid, else None."""
        user = await self.repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

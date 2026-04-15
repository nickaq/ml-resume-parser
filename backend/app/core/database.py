"""
Database session and engine configuration.
Supports both SQLite (local dev) and PostgreSQL (production).
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings

settings = get_settings()

# ── Async engine & session factory ───────────────────────────────
_engine_kwargs: dict = {
    "echo": settings.DEBUG,
}

if settings.USE_SQLITE:
    # SQLite requires check_same_thread=False for async usage
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
else:
    # PostgreSQL-specific pool settings
    _engine_kwargs["pool_pre_ping"] = True
    _engine_kwargs["pool_size"] = 10
    _engine_kwargs["max_overflow"] = 20

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session.
    Ensures the session is closed after each request.
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

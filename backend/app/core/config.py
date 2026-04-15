"""
Application configuration loaded from environment variables.
Uses pydantic-settings for validation and default values.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Application ──────────────────────────────────────────────
    APP_NAME: str = "ML Resume Parser"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # ── Database ─────────────────────────────────────────────────
    # Set USE_SQLITE=true for local development (no PostgreSQL needed)
    USE_SQLITE: bool = True
    SQLITE_PATH: str = "resume_parser.db"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "resume_parser"

    @property
    def DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return f"sqlite+aiosqlite:///{self.SQLITE_PATH}"
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SYNC_DATABASE_URL(self) -> str:
        if self.USE_SQLITE:
            return f"sqlite:///{self.SQLITE_PATH}"
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ── JWT / Auth ───────────────────────────────────────────────
    JWT_SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # ── CORS ─────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:3000,http://frontend:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    # ── AI / Matching ────────────────────────────────────────────
    # Default matching strategy. One of: keyword, tfidf, embeddings
    MATCHING_STRATEGY: str = "keyword"
    # Sentence-transformer model name (only used when strategy=embeddings)
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"


@lru_cache
def get_settings() -> Settings:
    """Cached singleton — avoids re-parsing .env on every import."""
    return Settings()

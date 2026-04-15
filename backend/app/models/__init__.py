"""Re-export all models for convenient imports."""

from app.models.recommendation import Recommendation  # noqa: F401
from app.models.resume import Resume  # noqa: F401
from app.models.user import User  # noqa: F401
from app.models.vacancy import Vacancy  # noqa: F401

# Import Base so Alembic can see it
from app.models.base import Base  # noqa: F401

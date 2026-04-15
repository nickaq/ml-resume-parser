"""Re-export all repositories."""

from app.repositories.base import BaseRepository  # noqa: F401
from app.repositories.recommendation_repository import RecommendationRepository  # noqa: F401
from app.repositories.resume_repository import ResumeRepository  # noqa: F401
from app.repositories.user_repository import UserRepository  # noqa: F401
from app.repositories.vacancy_repository import VacancyRepository  # noqa: F401

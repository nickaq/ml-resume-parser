"""
Vacancy model — represents a job posting.
Will be matched against resumes by the AI recommendation engine.
"""

from sqlalchemy import JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Vacancy(TimestampMixin, Base):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    experience_level: Mapped[str | None] = mapped_column(String(50), nullable=True)
    salary_min: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    salary_max: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default="true")
    
    required_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    nice_to_have_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    industry_domain: Mapped[str | None] = mapped_column(String(100), nullable=True)
    tools_stack: Mapped[list | None] = mapped_column(JSON, nullable=True)
    languages_stack: Mapped[list | None] = mapped_column(JSON, nullable=True)
    human_languages: Mapped[list | None] = mapped_column(JSON, nullable=True)
    work_format: Mapped[str | None] = mapped_column(String(50), nullable=True)

    def __repr__(self) -> str:
        return f"<Vacancy(id={self.id}, title={self.title}, company={self.company})>"

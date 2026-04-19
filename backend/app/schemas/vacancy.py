"""
Vacancy Pydantic schemas for request/response validation.
"""

from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class VacancyCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    requirements: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    salary_min: Decimal | None = Field(None, ge=0)
    salary_max: Decimal | None = Field(None, ge=0)
    url: str | None = None
    required_skills: list[str] | None = None
    nice_to_have_skills: list[str] | None = None
    industry_domain: str | None = None
    tools_stack: list[str] | None = None
    languages_stack: list[str] | None = None
    human_languages: list[str] | None = None
    work_format: str | None = None

class VacancyUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    company: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    requirements: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    salary_min: Decimal | None = Field(None, ge=0)
    salary_max: Decimal | None = Field(None, ge=0)
    url: str | None = None
    is_active: bool | None = None
    required_skills: list[str] | None = None
    nice_to_have_skills: list[str] | None = None
    industry_domain: str | None = None
    tools_stack: list[str] | None = None
    languages_stack: list[str] | None = None
    human_languages: list[str] | None = None
    work_format: str | None = None
class VacancyResponse(BaseModel):
    id: int
    title: str
    company: str
    description: str
    requirements: str | None = None
    location: str | None = None
    employment_type: str | None = None
    experience_level: str | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    url: str | None = None
    is_active: bool
    required_skills: list[str] | None = None
    nice_to_have_skills: list[str] | None = None
    industry_domain: str | None = None
    tools_stack: list[str] | None = None
    languages_stack: list[str] | None = None
    human_languages: list[str] | None = None
    work_format: str | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

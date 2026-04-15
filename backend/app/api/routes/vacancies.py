"""
Vacancy routes — CRUD for job vacancies.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.vacancy import VacancyCreate, VacancyResponse, VacancyUpdate
from app.services.vacancy_service import VacancyService
from app.utils.helpers import filter_none

router = APIRouter(prefix="/vacancies", tags=["vacancies"])


@router.post("", response_model=VacancyResponse, status_code=status.HTTP_201_CREATED)
async def create_vacancy(
    payload: VacancyCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Create a new vacancy (admin / recruiter action)."""
    service = VacancyService(db)
    return await service.create(**payload.model_dump())


@router.get("", response_model=list[VacancyResponse])
async def list_vacancies(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    search: str | None = Query(None, min_length=1),
):
    """List active vacancies. Optional `search` filters by title, company, or description."""
    service = VacancyService(db)
    if search:
        return await service.search(query=search, skip=skip, limit=limit)
    return await service.get_active(skip=skip, limit=limit)


@router.get("/{vacancy_id}", response_model=VacancyResponse)
async def get_vacancy(
    vacancy_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    """Get a single vacancy by ID."""
    service = VacancyService(db)
    vacancy = await service.get_by_id(vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    return vacancy


@router.patch("/{vacancy_id}", response_model=VacancyResponse)
async def update_vacancy(
    vacancy_id: int,
    payload: VacancyUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Update a vacancy."""
    service = VacancyService(db)
    updated = await service.update(vacancy_id, filter_none(payload.model_dump()))
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")
    return updated


@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(
    vacancy_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Delete a vacancy."""
    service = VacancyService(db)
    deleted = await service.delete(vacancy_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vacancy not found")

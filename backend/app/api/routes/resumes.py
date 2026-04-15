"""
Resume routes — upload, list, get, and delete resumes.
Supports file upload via multipart/form-data.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.resume import ResumeResponse
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Invalid file type or size"},
        422: {"description": "Validation error"},
    },
)
async def upload_resume(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
    file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
):
    """
    Upload a resume file. The file will be saved and its text extracted automatically.

    Supported formats: `.pdf`, `.docx`, `.txt`
    Maximum file size: 10 MB
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Filename is required",
        )

    service = ResumeService(db)
    try:
        resume = await service.upload_resume(user_id=current_user.id, file=file)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return resume


@router.get("", response_model=list[ResumeResponse])
async def list_resumes(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """List all resumes for the authenticated user."""
    service = ResumeService(db)
    return await service.get_by_user(user_id=current_user.id)


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Get a specific resume by ID (must belong to the user)."""
    service = ResumeService(db)
    resume = await service.get_by_id(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    return resume


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    """Delete a resume and its stored file."""
    service = ResumeService(db)
    deleted = await service.delete(resume_id=resume_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

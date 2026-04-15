"""
Resume service — handles resume upload, file storage, and text extraction.
"""

from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resume import Resume
from app.repositories.resume_repository import ResumeRepository
from app.services.file_storage import delete_file, generate_filename, save_file
from app.services.text_extraction import extract_text_from_file

# Maximum file size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed MIME types / extensions
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


class ResumeService:
    def __init__(self, db: AsyncSession):
        self.repo = ResumeRepository(db)

    async def upload_resume(
        self, user_id: int, file: UploadFile
    ) -> Resume:
        """
        Process a resume upload:
        1. Validate file type and size
        2. Save file to disk
        3. Extract text from file
        4. Store resume record in database
        """
        # Validate extension
        ext = Path(file.filename or "").suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: '{ext}'. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        # Read file content to check size
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise ValueError(
                f"File too large ({len(contents) / 1024 / 1024:.1f} MB). "
                f"Maximum size: {MAX_FILE_SIZE / 1024 / 1024:.0f} MB"
            )

        # Reset file pointer for downstream consumers
        await file.seek(0)

        # Save file to disk
        unique_filename = generate_filename(file.filename or "resume")
        file_path = await save_file(file, unique_filename)

        try:
            # Extract text from the saved file
            extracted_text = extract_text_from_file(file_path, file.filename or "")
        except (ValueError, RuntimeError):
            # If extraction fails, delete the file and re-raise
            delete_file(file_path)
            raise

        # Store in database
        return await self.repo.create({
            "user_id": user_id,
            "original_filename": file.filename or "unknown",
            "file_path": str(file_path),
            "extracted_text": extracted_text,
        })

    async def get_by_user(self, user_id: int) -> list[Resume]:
        """Get all resumes for a user."""
        return await self.repo.get_by_user(user_id)

    async def get_by_id(self, resume_id: int) -> Resume | None:
        return await self.repo.get_by_id(resume_id)

    async def delete(self, resume_id: int, user_id: int) -> bool:
        """Delete a resume and its file from disk."""
        resume = await self.repo.get_by_id(resume_id)
        if not resume or resume.user_id != user_id:
            return False
        # Delete file from disk
        delete_file(resume.file_path)
        await self.repo.delete(resume)
        return True

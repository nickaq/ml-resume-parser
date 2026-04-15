"""
Resume Pydantic schemas for request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    user_id: int
    original_filename: str
    file_path: str
    extracted_text: str | None = None
    uploaded_at: datetime

    model_config = {"from_attributes": True}

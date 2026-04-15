"""
Resume model — stores uploaded resume files and extracted text.
The AI service will later parse extracted_text into structured data.
"""

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    extracted_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    uploaded_at: Mapped[str] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Future AI-enriched fields:
    # parsed_skills: Mapped[str | None] = mapped_column(Text, nullable=True)
    # experience_years: Mapped[int | None] = mapped_column(nullable=True)
    # education: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, user_id={self.user_id}, file={self.original_filename})>"
